import os
import subprocess
import argparse
from datetime import datetime
import sys

# ✅ Setup argument parser
parser = argparse.ArgumentParser(description="Run Pytest tests with environment and reporting options.")
parser.add_argument("--env", type=str, default="DEV", choices=["DEV", "UAT", "PROD"],
                    help="Set the test environment (DEV, UAT, PROD). Defaults to 'DEV'.")
parser.add_argument("--tests", type=str, default="Testcases/",
                    help="Specify the test file or directory to run. Defaults to 'Testcases/'.")
parser.add_argument("--headless", action="store_true",
                    help="Run tests in headless mode")

args = parser.parse_args()

env = args.env.upper()  # Ensure uppercase for consistency
tests_to_run = args.tests
headless_flag = "--headless" if args.headless else ""  # ✅ Enable headless mode if passed

# ✅ Explicitly set the environment variable in the OS
os.environ["ENVIRONMENT"] = env  # This ensures that all Python modules read the correct ENV
PYTHON_EXECUTABLE = sys.executable  # Gets the current Python interpreter path

# ✅ Generate a timestamped report folder
REPORTS_DIR = "Reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_folder = os.path.join(REPORTS_DIR, f"test_report_{env}_{timestamp}")

# ✅ Display the test execution details
print(f"🚀 Running tests in environment: {env}")
print(f"📂 Test location: {tests_to_run}")
print(f"📄 Report will be generated in: {report_folder}")
print(f"🖥️ Headless Mode: {'Enabled' if args.headless else 'Disabled'}")

# ✅ Run Pytest with dynamic parameters
exit_code = subprocess.run(
    [
        PYTHON_EXECUTABLE, "-m", "pytest",
        tests_to_run,
        "-v",  # 👈 Add verbose flag to see test execution details
        "--tb=short",
        "--capture=sys",
        "--html-report", report_folder,
        f"--env={env}",
        headless_flag
    ],
    shell=True,
).returncode


# ✅ Print success/failure message
if exit_code == 0:
    print(f"\n✅ Test execution completed successfully. Report generated in folder: {report_folder}")
else:
    print(f"\n❌ Test execution failed. Check logs for details. Report generated in folder: {report_folder}")

exit(exit_code)














# import os
# import subprocess
# import argparse
# from datetime import datetime
# import sys
#
# # ✅ Setup argument parser
# parser = argparse.ArgumentParser(description="Run Pytest tests with environment and reporting options.")
# parser.add_argument("--env", type=str, default="DEV", choices=["DEV", "UAT", "PROD"],
#                     help="Set the test environment (DEV, UAT, PROD). Defaults to 'DEV'.")
# parser.add_argument("--tests", type=str, default="Testcases/",
#                     help="Specify the test file or directory to run. Defaults to 'Testcases/'.")
# parser.add_argument("--headless", action="store_true",
#                     help="Run tests in headless mode")
#
# args = parser.parse_args()
#
# env = args.env.upper()  # Ensure uppercase for consistency
# tests_to_run = args.tests
# headless_flag = "--headless" if args.headless else ""  # ✅ Enable headless mode if passed
#
# # ✅ Explicitly set the environment variable in the OS
# os.environ["ENVIRONMENT"] = env  # This ensures that all Python modules read the correct ENV
# PYTHON_EXECUTABLE = sys.executable  # Gets the current Python interpreter path
#
# # ✅ Generate a timestamped report folder
# REPORTS_DIR = "Reports"
# os.makedirs(REPORTS_DIR, exist_ok=True)
#
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# report_folder = os.path.join(REPORTS_DIR, f"test_report_{env}_{timestamp}")
#
# # ✅ Display the test execution details
# print(f"🚀 Running tests in environment: {env}")
# print(f"📂 Test location: {tests_to_run}")
# print(f"📄 Report will be generated in: {report_folder}")
# print(f"🖥️ Headless Mode: {'Enabled' if args.headless else 'Disabled'}")
#
# # ✅ Run Pytest with dynamic parameters
# exit_code = subprocess.run(
#     [
#         PYTHON_EXECUTABLE, "-m", "pytest",
#         tests_to_run,
#         "--tb=short",
#         "--capture=sys",
#         "--html-report", report_folder,
#         f"--env={env}",
#         headless_flag  # ✅ Add headless mode flag dynamically
#     ],
#     shell=True,
# ).returncode
#
# # ✅ Print success/failure message
# if exit_code == 0:
#     print(f"\n✅ Test execution completed successfully. Report generated in folder: {report_folder}")
# else:
#     print(f"\n❌ Test execution failed. Check Logs for details. Report generated in folder: {report_folder}")
#
# exit(exit_code)
#
























# import os
# import subprocess
# import argparse
# from datetime import datetime
# import sys
#
#
# # ✅ Setup argument parser
# parser = argparse.ArgumentParser(description="Run Pytest tests with environment and reporting options.")
# parser.add_argument("--env", type=str, default="DEV", choices=["DEV", "UAT", "PROD"],
#                     help="Set the test environment (DEV, UAT, PROD). Defaults to 'DEV'.")
# parser.add_argument("--tests", type=str, default="Testcases/",
#                     help="Specify the test file or directory to run. Defaults to 'Testcases/'.")
# args = parser.parse_args()
#
# env = args.env.upper()  # Ensure uppercase for consistency
# tests_to_run = args.tests
#
# # ✅ Explicitly set the environment variable in the OS
# os.environ["ENVIRONMENT"] = env  # This ensures that all Python modules read the correct ENV
# PYTHON_EXECUTABLE = sys.executable  # Gets the current Python interpreter path
# # ✅ Generate a timestamped report folder
# REPORTS_DIR = "Reports"
# os.makedirs(REPORTS_DIR, exist_ok=True)
#
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# report_folder = os.path.join(REPORTS_DIR, f"test_report_{env}_{timestamp}")
#
# # ✅ Display the test execution details
# print(f"🚀 Running tests in environment: {env}")
# print(f"📂 Test location: {tests_to_run}")
# print(f"📄 Report will be generated in: {report_folder}")
#
# # ✅ Define the correct execution order
# test_execution_order = [
#     "Testcases/test_login_screen.py",        # ✅ First: Login tests
#     "Testcases/test_dashboard_screen.py"     # ✅ Second: Dashboard tests
# ]
#
# # ✅ Run Pytest with explicit ordering
# exit_code = subprocess.run(
#     [
#         PYTHON_EXECUTABLE, "-m", "pytest",
#         *test_execution_order,  # Pass files explicitly in defined order
#         "--tb=short",
#         "--capture=sys",
#         "--html-report", report_folder,
#         f"--env={env}"
#     ],
#     shell=True,
# ).returncode
# # ✅ Print success/failure message
# if exit_code == 0:
#     print(f"\n✅ Test execution completed successfully. Report generated in folder: {report_folder}")
# else:
#     print(f"\n❌ Test execution failed. Check Logs for details. Report generated in folder: {report_folder}")
#
# exit(exit_code)








# import os
# import subprocess
# import argparse
# from datetime import datetime
# import sys
#
# # Ensure we're using the correct Python executable
# PYTHON_EXECUTABLE = sys.executable  # Gets the current Python interpreter path
#
# # Create a Reports directory if it doesn't exist
# REPORTS_DIR = "Reports"
# if not os.path.exists(REPORTS_DIR):
#     os.makedirs(REPORTS_DIR)
#
# # Generate a timestamped report folder
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# report_folder = os.path.join(REPORTS_DIR, f"test_report_{timestamp}")
#
# # Setup argument parser
# parser = argparse.ArgumentParser(description="Run Pytest tests with environment and reporting options.")
# parser.add_argument("--env", type=str, default="DEV", choices=["DEV", "UAT", "PROD"],
#                     help="Set the test environment (DEV, UAT, PROD). Defaults to 'DEV'.")
# parser.add_argument("--tests", type=str, default="Testcases/",
#                     help="Specify the test file or directory to run. Defaults to 'Testcases/'.")
# args = parser.parse_args()
#
# env = args.env.upper()  # Ensure uppercase for consistency
# tests_to_run = args.tests
#
# # Display the test execution details
# print(f"🚀 Running tests in environment: {env}")
# print(f"📂 Test location: {tests_to_run}")
# print(f"📄 Report will be generated in: {report_folder}")
#
# # Run Pytest with dynamic parameters
# exit_code = subprocess.run(
#     [
#         PYTHON_EXECUTABLE, "-m", "pytest",  # Run inside virtual environment
#         tests_to_run,  # Run specified test file or folder
#         "--tb=short",  # Show short traceback
#         "--capture=sys",  # Capture stdout and stderr
#         "--html-report", report_folder,  # Use pytest-html-reporter
#         f"--env={env}"  # Pass the environment parameter dynamically
#     ],
#     shell=True,
# ).returncode
#
# # Print success/failure message
# if exit_code == 0:
#     print(f"\n✅ Test execution completed successfully. Report generated in folder: {report_folder}")
# else:
#     print(f"\n❌ Test execution failed. Check Logs for details. Report generated in folder: {report_folder}")
#
# exit(exit_code)
#
#
# # python main.py --env PROD
# # pytest --env PROD
