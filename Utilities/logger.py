import logging
import os
import shutil
from datetime import datetime


def get_environment():
    """ ✅ Always fetch the latest environment value dynamically. """
    return os.getenv("ENVIRONMENT", "DEV").upper()  # ✅ Always read fresh ENV value


def setup_logger(logger_name="TestLogger"):
    """ ✅ Creates and configures a logger with the correct ENV dynamically. """

    ENV = get_environment()  # ✅ Fetch the latest ENV dynamically
    LOG_DIR = os.path.join("Logs", ENV)  # ✅ Ensure correct log directory
    ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")

    # ✅ Generate a timestamped log file with the correct ENV name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LOG_FILE = os.path.join(LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")  # ✅ Fixed file path

    # ✅ Ensure directory structure exists
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # ✅ Archive old Logs before starting a new log
    for file in os.listdir(LOG_DIR):
        if file.endswith(".log") and not file.startswith("archive"):
            old_log_path = os.path.join(LOG_DIR, file)
            new_archive_path = os.path.join(ARCHIVE_DIR, file)
            shutil.move(old_log_path, new_archive_path)

    # ✅ Setup the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # ✅ Remove old handlers to avoid duplicate Logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # File Handler - Logs stored per test execution
    file_handler = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))

    # Console Handler - Logs shown in console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    # ✅ Add Handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"🚀 Logger initialized for environment: {ENV}")
    logger.info(f"📂 Log file: {LOG_FILE}")

    return logger


# ✅ Fetch the latest ENV dynamically every time a new logger is created
logger = setup_logger()
























#
# import logging
# import os
# import shutil
# from datetime import datetime
#
# def setup_logger(logger_name="TestLogger", level=logging.INFO):
#     """
#     ✅ Creates and configures a logger with file and console handlers.
#     """
#     # ✅ Fetch the environment dynamically when the logger is initialized
#     ENV = os.getenv("ENVIRONMENT", "DEV").upper()  # Default to DEV if not set
#
#     # ✅ Define log directory structure
#     LOG_DIR = "Logs"
#     ENV_LOG_DIR = os.path.join(LOG_DIR, ENV)  # Separate Logs per environment
#     ARCHIVE_DIR = os.path.join(ENV_LOG_DIR, "archive")  # Archive folder inside each environment log folder
#
#     # ✅ Generate a timestamped log file for every test run
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     LOG_FILE = os.path.join(ENV_LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")

    # def archive_old_logs():
    #     """Move previous log files to archive before starting a new log."""
    #     os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
    #     for file in os.listdir(ENV_LOG_DIR):
    #         if file.endswith(".log") and not file.startswith("archive"):
    #             old_log_path = os.path.join(ENV_LOG_DIR, file)
    #             new_archive_path = os.path.join(ARCHIVE_DIR, file)
    #             shutil.move(old_log_path, new_archive_path)  # Move log file to archive
    #
    # # ✅ Ensure environment-specific log directory exists
    # os.makedirs(ENV_LOG_DIR, exist_ok=True)
    # archive_old_logs()  # Archive previous Logs
    #
    # logger = logging.getLogger(logger_name)
    # logger.setLevel(level)
    #
    # # Prevent duplicate handlers
    # if not logger.handlers:
    #     # File Handler - Logs stored per test execution
    #     file_handler = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
    #     file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
    #
    #     # Console Handler - Logs shown in console
    #     console_handler = logging.StreamHandler()
    #     console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    #
    #     # Add Handlers
    #     logger.addHandler(file_handler)
    #     logger.addHandler(console_handler)

#     # ✅ Initialize global logger
#     logger.info(f"🚀 Logger initialized for environment: {ENV}")
#     logger.info(f"📂 Log file: {LOG_FILE}")
#
#     return logger
#
# logger = setup_logger()







# import logging
# import os
# import shutil
# from datetime import datetime
#
# # ✅ Ensure ENVIRONMENT is set before raising an error
# ENV = os.getenv("ENVIRONMENT", "DEV").upper()  # Default to "DEV" if not set
#
# # ✅ Define log directory structure
# LOG_DIR = "Logs"
# ENV_LOG_DIR = os.path.join(LOG_DIR, ENV)  # Separate Logs per environment
# ARCHIVE_DIR = os.path.join(ENV_LOG_DIR, "archive")  # Archive folder inside each environment log folder
#
# # ✅ Generate a timestamped log file for every test run
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# LOG_FILE = os.path.join(ENV_LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")
#
#
# def archive_old_logs():
#     """Move previous log files to archive before starting a new log."""
#     os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
#
#     for file in os.listdir(ENV_LOG_DIR):
#         if file.endswith(".log") and not file.startswith("archive"):
#             old_log_path = os.path.join(ENV_LOG_DIR, file)
#             new_archive_path = os.path.join(ARCHIVE_DIR, file)
#             shutil.move(old_log_path, new_archive_path)  # Move log file to archive
#
#
# def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
#     """
#     ✅ Creates and configures a logger with file and console handlers.
#     """
#     os.makedirs(ENV_LOG_DIR, exist_ok=True)  # Ensure environment-specific log directory exists
#     archive_old_logs()  # Archive previous Logs
#
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#
#     # Prevent duplicate handlers
#     if not logger.handlers:
#         # File Handler - Logs stored per test execution
#         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
#         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
#
#         # Console Handler - Logs shown in console
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#         # Add Handlers
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     return logger
#
#
# # ✅ Initialize global logger
# logger = setup_logger()
# logger.info(f"🚀 Logger initialized for environment: {ENV}")
# logger.info(f"📂 Log file: {LOG_FILE}")
#
#
#








# import logging
# import os
# import shutil
# from datetime import datetime
#
# # ✅ Get the environment from system variables
# ENV = os.getenv("ENVIRONMENT")  # Read dynamically
# if not ENV:
#     raise ValueError("❌ ERROR: Environment not set! Please provide ENVIRONMENT (DEV, UAT, PROD).")
#
# ENV = ENV.upper()  # Ensure uppercase consistency
#
# # ✅ Define log directory structure
# LOG_DIR = "Logs"
# ENV_LOG_DIR = os.path.join(LOG_DIR, ENV)  # Separate Logs per environment
# ARCHIVE_DIR = os.path.join(ENV_LOG_DIR, "archive")  # Archive folder inside each environment log folder
#
# # ✅ Generate a timestamped log file for every test run
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# LOG_FILE = os.path.join(ENV_LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")
#
#
# def archive_old_logs():
#     """Move previous log files to archive before starting a new log."""
#     os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
#
#     for file in os.listdir(ENV_LOG_DIR):
#         if file.endswith(".log") and not file.startswith("archive"):
#             old_log_path = os.path.join(ENV_LOG_DIR, file)
#             new_archive_path = os.path.join(ARCHIVE_DIR, file)
#             shutil.move(old_log_path, new_archive_path)  # Move log file to archive
#
#
# def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
#     """
#     Creates and configures a logger with file and console handlers.
#     """
#     os.makedirs(ENV_LOG_DIR, exist_ok=True)  # Ensure environment-specific log directory exists
#     archive_old_logs()  # Archive previous Logs
#
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#
#     # Prevent duplicate handlers
#     if not logger.handlers:
#         # File Handler - Logs stored per test execution
#         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
#         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
#
#         # Console Handler - Logs shown in console
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#         # Add Handlers
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     return logger
#
#
# # ✅ Initialize global logger
# logger = setup_logger()
# logger.info(f"🚀 Logger initialized for environment: {ENV}")
# logger.info(f"📂 Log file: {LOG_FILE}")
#





# import logging
# import os
# import shutil
# from datetime import datetime
#
# # ✅ Get the environment from system variables, default to "DEV" if not set
# ENV = os.getenv("ENVIRONMENT", "DEV").upper()
#
# # ✅ Define log directory structure
# LOG_DIR = "Logs"
# ENV_LOG_DIR = os.path.join(LOG_DIR, ENV)  # Separate Logs per environment
# ARCHIVE_DIR = os.path.join(ENV_LOG_DIR, "archive")  # Archive folder inside each environment log folder
#
# # ✅ Generate a timestamped log file for every test run
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# LOG_FILE = os.path.join(ENV_LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")
#
#
# def archive_old_logs():
#     """Move all previous Logs to the archive before creating a new log."""
#     os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
#
#     for file in os.listdir(ENV_LOG_DIR):
#         if file.endswith(".log") and not file.startswith("archive"):
#             old_log_path = os.path.join(ENV_LOG_DIR, file)
#             new_archive_path = os.path.join(ARCHIVE_DIR, file)
#             shutil.move(old_log_path, new_archive_path)  # Move log file to archive
#
#
# def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
#     """
#     Creates and configures a logger with file and console handlers.
#     """
#     os.makedirs(ENV_LOG_DIR, exist_ok=True)  # Ensure environment-specific log directory exists
#     archive_old_logs()  # Archive previous Logs
#
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#
#     # Prevent duplicate handlers
#     if not logger.handlers:
#         # File Handler - Logs stored per test execution
#         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
#         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
#
#         # Console Handler - Logs shown in console
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#         # Add Handlers
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     return logger
#
#
# # ✅ Initialize global logger
# logger = setup_logger()
# logger.info(f"🚀 Logger initialized for environment: {ENV}")
# logger.info(f"📂 Log file: {LOG_FILE}")




# import logging
# import os
# import shutil
# from datetime import datetime
#
# # ✅ Get environment from system variables (Set in main.py)
# ENV = os.getenv("ENVIRONMENT")  # Ensure it's read dynamically from system environment
# if not ENV:
#     raise ValueError("❌ ERROR: Environment not set! Please provide ENVIRONMENT (DEV, UAT, PROD).")
#
# ENV = ENV.upper()  # Ensure it's uppercase
#
# # ✅ Define log directory structure
# LOG_DIR = "Logs"
# ENV_LOG_DIR = os.path.join(LOG_DIR, ENV)  # Separate Logs per environment
# ARCHIVE_DIR = os.path.join(ENV_LOG_DIR, "archive")  # Archive folder inside each environment log folder
#
# # ✅ Generate a timestamped log file for every test run
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# LOG_FILE = os.path.join(ENV_LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")
#
#
# def archive_old_logs():
#     """Move the previous log file to the archive directory before creating a new log."""
#     if os.path.exists(LOG_FILE):
#         os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
#         archived_log = os.path.join(ARCHIVE_DIR, f"{ENV}_test_logs_{timestamp}.log")
#         shutil.move(LOG_FILE, archived_log)  # Move log file to archive
#
#
# def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
#     """
#     Creates and configures a logger with file and console handlers.
#     """
#     os.makedirs(ENV_LOG_DIR, exist_ok=True)  # Ensure environment-specific log directory exists
#     archive_old_logs()  # Archive previous Logs
#
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#
#     # Prevent duplicate handlers
#     if not logger.handlers:
#         # File Handler - Logs stored per test execution
#         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
#         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
#
#         # Console Handler - Logs shown in console
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#         # Add Handlers
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     return logger
#
#
# # ✅ Initialize global logger
# logger = setup_logger()
# logger.info(f"🚀 Logger initialized for environment: {ENV}")
# logger.info(f"📂 Log file: {LOG_FILE}")
#
#
#


# import logging
# import os
# import shutil
# from datetime import datetime
#
# # ✅ Get environment from system variables (Set in main.py)
# ENV = os.getenv("ENVIRONMENT", "DEV").upper()  # Read from ENV variable
#
# LOG_DIR = "Logs"
# ENV_LOG_DIR = os.path.join(LOG_DIR, ENV)  # Separate Logs per environment
# ARCHIVE_DIR = os.path.join(ENV_LOG_DIR, "archive")  # Archive folder inside each environment log folder
#
# # ✅ Include date & time in log file name
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# LOG_FILE = os.path.join(ENV_LOG_DIR, f"{ENV}_test_logs_{timestamp}.log")
#
#
# def archive_old_logs():
#     """Move all existing Logs to the archive directory before starting a new log session."""
#     if not os.path.exists(ENV_LOG_DIR):
#         return  # No log directory exists yet, so nothing to archive
#
#     os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
#
#     for file in os.listdir(ENV_LOG_DIR):
#         if file.endswith(".log") and not file.startswith("archive"):  # Move only log files
#             old_log_path = os.path.join(ENV_LOG_DIR, file)
#             new_archive_path = os.path.join(ARCHIVE_DIR, file)
#             shutil.move(old_log_path, new_archive_path)  # Move log file to archive
#
#
# def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
#     """
#     Creates and configures a logger with file and console handlers.
#     """
#     os.makedirs(ENV_LOG_DIR, exist_ok=True)  # Ensure environment-specific log directory exists
#     archive_old_logs()  # Archive old Logs before starting a new session
#
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#
#     # Prevent duplicate handlers
#     if not logger.handlers:
#         # File Handler
#         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
#         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
#
#         # Console Handler
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#         # Add Handlers
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     return logger
#
#
# # Initialize global logger
# logger = setup_logger()
#
# # ✅ Print log file location for reference
# logger.info(f"Logging initialized. Log file: {LOG_FILE}")
#
#



# import logging
# import os
# import shutil
# from datetime import datetime
#
# LOG_DIR = "Logs"
# ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")
# LOG_FILE = os.path.join(LOG_DIR, "test_logs.log")
#
#
# def archive_old_log():
#     """Move the existing log file to the archive directory with a timestamp before creating a new log."""
#     if os.path.exists(LOG_FILE):
#         os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         archived_log = os.path.join(ARCHIVE_DIR, f"test_logs_{timestamp}.log")
#         shutil.move(LOG_FILE, archived_log)  # Move log file to archive
#
#
# def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
#     """
#     Creates and configures a logger with file and console handlers.
#     """
#     os.makedirs(LOG_DIR, exist_ok=True)  # Ensure log directory exists
#     archive_old_log()  # Archive the old log before starting a new session
#
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#
#     # Prevent duplicate handlers
#     if not logger.handlers:
#         # File Handler
#         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
#         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
#
#         # Console Handler
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#         # Add Handlers
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     return logger
#
#
# # Initialize global logger
# logger = setup_logger()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # import logging
# # import os
# #
# # LOG_DIR = "Logs"
# # LOG_FILE = os.path.join(LOG_DIR, "test_logs.log")
# #
# # def setup_logger(logger_name="TestLogger", log_file=LOG_FILE, level=logging.INFO):
# #     """
# #     Creates and configures a logger.
# #     """
# #     os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Ensure log directory exists
# #
# #     # Remove existing log file for fresh Logs on every run
# #     if os.path.exists(log_file):
# #         os.remove(log_file)
# #
# #     logger = logging.getLogger(logger_name)
# #     logger.setLevel(level)
# #
# #     # Prevent duplicate handlers
# #     if not logger.handlers:
# #         # File Handler
# #         file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
# #         file_handler.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s : %(name)s :%(message)s'))
# #
# #         # Console Handler
# #         console_handler = logging.StreamHandler()
# #         console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
# #
# #         # Add Handlers
# #         logger.addHandler(file_handler)
# #         logger.addHandler(console_handler)
# #
# #     return logger
# #
# #
# # # Initialize global logger
# # logger = setup_logger()
