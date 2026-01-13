import pathlib
import socket
import subprocess
import tempfile
import time

import ciocore.data as coredata
import ciocore.conductor_submit
import ciocore.config
import ciocore.file_utils
import ciocore.uploader

from . import Diagnostics, FileDataSetGenerator, ONE_MB, logger


class UploadDiagnostics(Diagnostics):
    """
    Base class to test Uploader functionality
    """

    TEST_CATEGORY = "Uploader Integration Test"
    TEST_DESCRIPTION = __doc__.strip()
    TEST_COUNT = 0

    PROVIDER_INSTANCE_TYPES = {
        "cw": "cw-xeonv3-4",
        "gcp": "n1-standard-4",
        "aws": "m5.4xlarge"
    }

    def __init__(self,
                 cloud_provider=None,
                 conductor_project="default",
                 file_dataset=FileDataSetGenerator.production_spread_files,
                 thread_count=None,
                 local_upload=True,
                 keep_files=False):

        super().__init__()

        self.cloud_provider = cloud_provider
        self.conductor_project = conductor_project
        self.file_dataset = file_dataset()
        self.thread_count = thread_count
        self.local_upload = local_upload
        self.keep_files = keep_files
        self.file_paths = []

        self.unique_location_id = f"{socket.gethostname()}_{time.time()}"

        # For local uploads, this is the only way to set the thread count
        if self.thread_count is not None:
            ciocore.config.set("thread_count", self.thread_count)

    def get_cloud_provider(self):

        coredata.init(product="all")
        instances = coredata.data()["instance_types"]
        return instances.provider

    def generate_bash_script(self, file_paths):

        bash_script_path = pathlib.Path(
            tempfile.gettempdir(), "upload_diagnostics_test.sh")
        
        posix_paths = []
        for p in file_paths:

            path_object = pathlib.Path(p)
            
            if path_object.drive:
                parts = ["/"] + list(path_object.parts[1:])            
                path_object = pathlib.Path(*parts)
            
            posix_paths.append(path_object.as_posix())

        joined_file_paths = " ".join([f'"{p}"' for p in posix_paths])

        with bash_script_path.open("w", newline="\n") as fh:

            fh.write(f"declare -a file_list=({joined_file_paths})\n\n")
            fh.write('for FILE in "${file_list[@]}"; do\n')
            fh.write('        if [ ! -f "$FILE" ]; then\n')
            fh.write(
                '                echo "ERROR: $FILE doesn\'t exist. Exiting."\n')
            fh.write('                exit 1\n')
            fh.write('        fi\n')
            fh.write('        done\n\n')
            fh.write('echo "All ${#file_list[@]} files exist."\n')

        logger.debug(f"Generated bash script at {bash_script_path}")
        return bash_script_path

    def submit_job(self):

        if self.cloud_provider is None:
            self.cloud_provider = self.get_cloud_provider()

        bash_script_path = pathlib.Path(self.generate_bash_script(self.file_paths))

        if bash_script_path.drive:
            parts = ["/"] + list(bash_script_path.parts[1:])            
            bash_script_path = pathlib.Path(*parts)
        
        cmd = f"bash {bash_script_path.as_posix()}"
        self.file_paths.append(bash_script_path.as_posix())

        job_args = {
            "job_title": f"[{self.TEST_CATEGORY} {self.TEST_INDEX}/{self.TEST_COUNT}] {self.TEST_DESCRIPTION}",
            "project": self.conductor_project,
            "instance_type": self.PROVIDER_INSTANCE_TYPES.get(self.cloud_provider),
            "local_upload": self.local_upload,
            "location": self.unique_location_id,
            "preemptible": False,
            "output_path": "/uploader_integration_test_output/bob.txt",
            "upload_paths": self.file_paths,
            "tasks_data": [

                {'command': cmd,
                 'frames': '1'
                 }]
        }

        logger.debug("Submitting job with args: {}".format(job_args))
        submission = ciocore.conductor_submit.Submit(job_args)
        result, return_code = submission.main()
        logger.debug(result)

        if return_code != 201:
            raise Exception(
                f"Job submission failed: {result},(return code: {return_code})")

        return result

    def run(self):
        raise NotImplementedError("Subclasses must implement this method")

    def clean_up(self):

        if not self.keep_files:

            logger.debug(f"Cleaning up {len(self.file_paths)} temporary files...")

            for path in self.file_paths:
                logger.debug(f"Removing file {path}")
                pathlib.Path(path).unlink()

            pathlib.Path(self.file_paths[0]).parent.rmdir()
        
        else:
            logger.debug(f"NOT Cleaning up {len(self.file_paths)} temporary files...")


class UploadDiagnostics_TEST_1(UploadDiagnostics):
    """
    Submit a job and use the Uploader in daemon mode.
    """

    TEST_INDEX = 1
    TEST_DESCRIPTION = __doc__.strip()

    def __init__(self, *args, **kwargs):
        super().__init__(local_upload=False, *args, **kwargs)

    def run(self):

        self.log_test_start("Integration Upload Test",
                            self.TEST_INDEX, self.TEST_DESCRIPTION)

        self.log_test_step("Generating files...")
        self.file_paths = self.file_dataset.generate_random_files()
        file_count = len(self.file_paths)
        self.log_test_step(
            f"Files generated ({file_count} files, {self.file_dataset.total_size / ONE_MB} MB total)")
        job_result = self.submit_job()
        self.log_test_step("Job submitted")
        self.log_test_step("Starting Upload daemon in background...")

        # This needs to be a DEBUG otherwise the line to catch below won't appear and the daemon won't be shutdown
        uploader_args = ["conductor", "upload", "--log_to_console",
                         "--location", self.unique_location_id, "--log_level", "DEBUG"]

        if self.thread_count is not None:
            uploader_args += ["--thread-count", str(self.thread_count)]

        daemon_process = subprocess.Popen(uploader_args,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          text=True)

        while True:
            line = daemon_process.stdout.readline()
            logger.debug(line.strip())

            if "Upload of entity " in line:

                if "failed with errors." in line:
                    self.log_test_step(
                        "Upload encountered errors. Check logs for details.")
                    
                    raise Exception("Upload Daemon reported errors during upload Stopping tests.")
                    
                else:
                    self.log_test_step(
                        "Upload completed. Shutting down Upload Daemon...")
                    daemon_process.terminate()
                    self.log_test_step("Upload Daemon shutdown")
                    break
            
            if not line:
                break

        self.clean_up()
        self.log_test_step(
            f"{self.TEST_CATEGORY} #{self.TEST_INDEX} completed. Please verify that job {job_result['jid']} completed successfully in Conductor")


class UploadDiagnostics_TEST_2(UploadDiagnostics):
    """
    Test local upload job submission
    """

    TEST_INDEX = 2
    TEST_DESCRIPTION = __doc__.strip()

    def __init__(self, *args, **kwargs):
        super().__init__(local_upload=True, *args, **kwargs)

    def run(self):

        self.log_test_start("Integration Upload Test",
                            self.TEST_INDEX, self.TEST_DESCRIPTION)

        self.log_test_step("Generating files...")
        self.file_paths = self.file_dataset.generate_random_files()
        file_count = len(self.file_paths)
        self.log_test_step(
            f"Files generated ({file_count} files, {self.file_dataset.total_size / ONE_MB} MB total)")

        self.log_test_step("Submitting job...")
        job_result = self.submit_job()
        self.log_test_step("Job submitted")

        self.clean_up()
        self.log_test_step(
            f"{self.TEST_CATEGORY} #{self.TEST_INDEX} completed. Please verify that job {job_result['jid']} completed successfully in Conductor")


class UploadDiagnostics_TEST_3(UploadDiagnostics):
    """
    Test uploads with provided paths (no job)
    """

    TEST_INDEX = 3
    TEST_DESCRIPTION = __doc__.strip()

    def upload_files(self, file_paths):
        processed_filepaths = ciocore.file_utils.process_upload_filepaths(
            file_paths)
        file_map = {path: None for path in processed_filepaths}

        args_dict = {
            "database_filepath": None,
            "location": None,
            "md5_caching": True,
            "thread_count": ciocore.config.config().config['thread_count']
        }
        uploader = ciocore.uploader.Uploader(args_dict)
        uploader.handle_upload_response(project=None, upload_files=file_map)

    def run(self):

        self.log_test_start("Integration Upload Test",
                            self.TEST_INDEX, self.TEST_DESCRIPTION)

        self.log_test_step("Generating files...")
        self.file_paths = self.file_dataset.generate_random_files()
        file_count = len(self.file_paths)
        self.log_test_step(
            f"Files generated ({file_count} files, {self.file_dataset.total_size / ONE_MB} MB total)")

        self.log_test_step("Uploading files...")
        self.upload_files(self.file_paths)
        self.log_test_step("File upload completed")

        self.clean_up()
        self.log_test_step(
            f"{self.TEST_CATEGORY} #{self.TEST_INDEX} completed.")


class UploadDiagnostics_TEST_4(UploadDiagnostics_TEST_3):
    """
    Test against existing cached files
    """

    TEST_INDEX = 4
    TEST_DESCRIPTION = __doc__.strip()

    def __init__(self, file_dataset=FileDataSetGenerator.production_spread_files, *args, **kwargs):
        super().__init__(file_dataset=file_dataset, *args, **kwargs)
        self.cached_file_dataset = file_dataset()

    def run(self):

        self.log_test_start("Integration Upload Test",
                            self.TEST_INDEX, self.TEST_DESCRIPTION)

        self.log_test_step("Generating first set of files (to be cached)...")
        self.cached_paths = self.cached_file_dataset.generate_random_files()
        cached_file_count = len(self.cached_paths)
        self.log_test_step(
            f"Files generated ({cached_file_count} files, {self.cached_file_dataset.total_size / ONE_MB} MB total)")

        self.log_test_step("Generating second set of files (non-cached)...")
        self.file_paths = self.file_dataset.generate_random_files()
        file_count = len(self.file_paths)
        self.log_test_step(
            f"Files generated ({file_count} files, {self.file_dataset.total_size / ONE_MB} MB total)")

        logger.debug("Cached files: {}".format(
            self.cached_file_dataset.file_paths))
        logger.debug("New files: {}".format(self.file_dataset.file_paths))

        self.log_test_step("Uploading first set of files (to be cached)...")
        self.upload_files(self.cached_file_dataset.file_paths)
        self.log_test_step(
            "Uploading of first set of files (to be cached) completed")

        self.log_test_step("Submitting job with cached and new files...")
        self.file_paths = self.file_dataset.file_paths + \
            self.cached_file_dataset.file_paths
        job_result = self.submit_job()
        self.log_test_step("Job submission complete")

        self.clean_up()
        self.log_test_step(
            f"{self.TEST_CATEGORY} #{self.TEST_INDEX} completed. Please verify that job {job_result['jid']} completed successfully in Conductor")