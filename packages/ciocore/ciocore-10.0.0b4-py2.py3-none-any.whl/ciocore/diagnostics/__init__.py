import os
import random
import tempfile

# How output and logging is setup:
#
# All output is via the logging mechanism
#
# When running these tests, logging is hard-coded to only output INFO from the
# conductor.diagnostic log to the console. All other conductor logs are set to
# DEBUG and to be written to conductor_diagnostic.log in the specified log directory.
# If the log-level is set from the CLI, this will only affect conductor.diagnostic log
# messages sent to conductor_diagnostic.log
#
# When the upload daemon is used, log messages will be sent to its default log file
# as well as conductor_diagnostic.log. Nothing will be output in the console. The hard-coded
# level is also DEBUG.
#
# The motiviation is that everything will be self-contained within conductor_diagnostic.log
# and keep the console clean, while providijng the most detailed logs available by default.
logger = None

ONE_KB = 1024
ONE_MB = ONE_KB * 1024
ONE_GB = ONE_MB * 1024

DATA_SET_MAX_TOTAL_SIZE = 500*ONE_MB


class FileDataSetGenerator:
    """
    Generate a dataset of random files for testing.
    """

    DATA_SETS = {'production': 'production_spread_files',
                 'many_small': 'many_small_files',
                 'single_1MB': 'single_1MB_file',
                 'single_random': 'single_random_file'}

    def __init__(self,
                 min_files=1,
                 max_files=10,
                 min_size=ONE_MB,
                 max_size=ONE_GB,
                 temp_dir=None,
                 max_total_size=None):
        """
        Args:
            min_files (int): Minimum number of files to generate. Default is 1.
            max_files (int): Maximum number of files to generate. Default is 10.
            min_size (int): Minimum size of each file in bytes. Default is 1MB.
            max_size (int): Maximum size of each file in bytes.  Default is 1GB.
            temp_dir (str): Path to the temporary directory. If None, a new temp dir is created.
            max_total_size (int): Maximum total size of all files in bytes. If None, no limit.            
        """

        self.min_files = min_files
        self.max_files = max_files
        self.min_size = min_size
        self.max_size = max_size
        self.temp_dir = temp_dir
        self.max_total_size = max_total_size

        self.num_files = min_files if min_files == max_files else None
        self.file_paths = []
        self.total_size = 0  # bytes

    def generate_random_files(self):
        """
        Generate a random number of files with random sizes in a temporary directory.

        Returns:
            list: List of file paths generated.
        """

        if self.temp_dir is None:
            self.temp_dir = tempfile.mkdtemp()
        else:
            os.makedirs(self.temp_dir, exist_ok=True)

        if self.max_files != self.min_files:
            self.num_files = random.randint(self.min_files, self.max_files)

        last_file = False

        for i in range(self.num_files):
            file_size = random.randint(self.min_size, self.max_size)

            if ((self.max_total_size is not None) and
                    (self.total_size + file_size >= self.max_total_size)):
                file_size = self.max_total_size - self.total_size
                last_file = True

            file_path = os.path.join(self.temp_dir, f"random_file_{i}.bin")

            with open(file_path, "wb") as f:
                f.write(os.urandom(file_size))

            self.file_paths.append(file_path)
            self.total_size += file_size

            if last_file:
                break

        logger.debug("Generated {} files [{} bytes] in {}".format(
            len(self.file_paths), self.total_size, self.temp_dir))

        return self.file_paths

    @classmethod
    def single_random_file(cls, file_size=500*ONE_MB):
        """
        Create a FileDataSetGenerator object configured to generate a dataset 
        with a single random file of 500MB.

        Args:
            file_size (int): Size of the file in bytes. Default is 500MB.

        Returns: A FileDataSetGenerator instance.
        """

        return cls(min_files=1, max_files=1, min_size=file_size, max_size=file_size)

    @classmethod
    def single_1MB_file(cls):
        """
        Create a FileDataSetGenerator object configured to generate a dataset 
        with a single random file of 1MB.

        Returns: A FileDataSetGenerator instance.
        """
        return cls.single_random_file(file_size=ONE_MB)

    @classmethod
    def many_small_files(cls):
        """
        Create a FileDataSetGenerator object configured to generate a dataset 
        of 1000 small files (16KB-10MB). Total size won't exceed DATA_SET_MAX_TOTAL_SIZE.        

        Returns: A FileDataSetGenerator instance.
        """

        return cls(
            min_files=1000,
            max_files=1000,
            min_size=16*ONE_KB,
            max_size=10*ONE_MB,
            max_total_size=DATA_SET_MAX_TOTAL_SIZE
        )

    @classmethod
    def production_spread_files(cls):
        """
        Create a FileDataSetGenerator object configured to generate a random-sized
        dataset between 5 to 10,000 files. Files range in size from 16KB to 100MB.
        Total size won't exceed DATA_SET_MAX_TOTAL_SIZE.

        Returns: A FileDataSetGenerator instance.
        """

        return cls(min_files=5, max_files=10000, min_size=16*ONE_KB, max_size=100*ONE_MB, max_total_size=DATA_SET_MAX_TOTAL_SIZE)


class Diagnostics:
    """
    Base class for diagnostics tests.
    """

    TEST_INDEX = None
    TEST_DESCRIPTION = __doc__.strip()
    TEST_CATEGORY = None

    def log_test_start(self, category, index, message):
        """
        Log the start of a test. Intended to go to the console.

        Args:
            category (str): Test category.
            index (int): Test index.
            message (str): Test description.

        Returns: None
        """

        if self.thread_count is None:
            thread_message = "No threads specified. Using default"

        else:
            thread_message = f"Using {self.thread_count} threads"

        logger.info(f"[{category} #{index}] {message} ({thread_message})")

    def log_test_step(self, message):
        """
        Log a message for a distinct step within a test. Intended to go to the console.

        Args:
            message (str): Step description.

        Returns: None
        """

        logger.info(f"{'':>28}- {message}")

    def cleanup_temp_files(self, temp_dir):
        """ 
        Clean up the temporary files in the specified directory.

        Args:
            temp_dir (str): Path to the directory containing the temporary files.
        """
        if os.path.exists(temp_dir):

            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)

                try:
                    os.remove(file_path)
                except OSError as e:
                    logger.error(f"Error removing file {file_path}: {e}")

            os.rmdir(temp_dir)

        else:
            logger.warning(f"Directory {temp_dir} does not exist.")


class TestRunner(Diagnostics):
    """
    Run the suite of diagnostics tests.
    """

    def __init__(self, data_set, max_size, keep_files, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_set = getattr(FileDataSetGenerator, FileDataSetGenerator.DATA_SETS[data_set])
        global DATA_SET_MAX_TOTAL_SIZE
        DATA_SET_MAX_TOTAL_SIZE = max_size

        self.keep_files = keep_files

    def run(self):
        
        from . import upload_diagnostics

        upload_diagnostics.UploadDiagnostics.TEST_COUNT = 4
        upload_diagnostics.UploadDiagnostics_TEST_1(file_dataset=self.data_set, keep_files=self.keep_files).run()
        upload_diagnostics.UploadDiagnostics_TEST_2(file_dataset=self.data_set, keep_files=self.keep_files).run()
        upload_diagnostics.UploadDiagnostics_TEST_3(
            file_dataset=self.data_set, keep_files=self.keep_files).run()
        upload_diagnostics.UploadDiagnostics_TEST_4(file_dataset=self.data_set, keep_files=self.keep_files).run()
