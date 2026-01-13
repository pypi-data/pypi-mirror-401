#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import socket
import subprocess
import sys
import time
from urllib.parse import urljoin, urlparse


__PYTHON_VERSION = sys.version_info

# Compatibility imports and version check
if __PYTHON_VERSION >= (3, 8):
    CONCURRENCY_MODE = "asyncio"
elif __PYTHON_VERSION >= (3, 0):
    CONCURRENCY_MODE = "threading_py3"
else:
    CONCURRENCY_MODE = "threading_py2"

# do import
# HTTP library compatibility for Python 2.7 and 3.x
if __PYTHON_VERSION >= (3, 0):
    from urllib.request import urlopen, Request
else:
    from urllib2 import urlopen, Request, URLError

if CONCURRENCY_MODE == "asyncio":
    import asyncio
elif CONCURRENCY_MODE == "threading_py3":
    from concurrent.futures import ThreadPoolExecutor  # noqa
else:
    try:
        # Attempt to import Python 2.7 compatibility libraries
        from futures import ThreadPoolExecutor
        from Queue import Queue

    except ImportError:
        CONCURRENCY_MODE = "unsupported"

# Core
PY_INFO = sys.version_info
MAX_LATENCY = float("inf")

MAIN = [
    "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/",
    "https://repo.huaweicloud.com/repository/pypi/simple/",
    "https://mirrors.aliyun.com/pypi/simple/",
    "https://mirrors.ustc.edu.cn/pypi/simple/",
    "https://mirrors.cloud.tencent.com/pypi/simple/",
]

BACKUP = [
    # "https://pypi.doubanio.com/simple/",  # Deprecate,Response:302 to Tencent
    # "https://mirrors.163.com/pypi/simple/",  # Deprecate
    # "https://mirror.baidu.com/pypi/simple/",  # Response:403
]

ALL_MIRRORS = set(MAIN + BACKUP)

DEFAULT_INDEX_URL = "https://pypi.org/simple"
EXTRA_INDEX_URLS = []

# Test file configuration
TEST_PACKAGE_PATH = "packages/44/3c/d717024885424591d5376220b5e836c2d5293ce2011523c9de23ff7bf068/pip-25.3-py3-none-any.whl"
TEST_FILE_SIZE = 1024 * 4  # 4KB
TEST_COUNT = 3  # Number of consecutive tests
DOWNLOAD_SPEED_UNIT = "KB/s"  # Speed display unit


class MirrorTester:
    """
    A mirror source speed tester compatible with Python 2.7 to 3.x.
    Automatically selects asyncio (>=3.8) or ThreadPoolExecutor (<=3.7) based on Python version.
    """

    def __init__(self, urls, timeout=3.5, test_mode="by_content"):
        """
        Initialize MirrorTester.
        
        :param urls: List of mirror URLs to test.
        :param timeout: Request timeout in seconds.
        :param test_mode: Testing mode, can be "by_tcp" (v1) or "by_content" (v2).
        """
        self.urls = urls
        self.timeout = timeout
        self.test_method = test_mode
        self.results = []
        self.concurrency_mode = CONCURRENCY_MODE

        print(
            f"Detected Python Version: {PY_INFO.major}.{PY_INFO.minor}.{PY_INFO.micro} ({self.mode})"
        )
        print("=" * 40)

        self.__fastest_url = None

    @property
    def fastest_url(self):
        return self.__fastest_url

    @property
    def mode(self):
        return self.concurrency_mode

    def _parse_url(self, url):
        """Parse URL and return hostname and port."""
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or (443 if host.startswith("https://") else 80)
        if not host:
            raise ValueError(f"Invalid URL host: {url}")

        return host, port

    # --- v1: TCP Connection Test (by_tcp) ---

    def _test_connection_by_tcp_sync(self, url):
        """Test a single connection speed using synchronous socket (v1)."""
        try:
            host, port = self._parse_url(url)
            ip = socket.gethostbyname(host)
        except Exception:
            return url, MAX_LATENCY

        start_time = time.time()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:
            sock.connect((ip, port))
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            return url, round(latency, 2)
        except Exception:
            return url, MAX_LATENCY
        finally:
            sock.close()

    async def _test_connection_by_tcp_async(self, url):
        """Test a single connection speed using asyncio (v1)."""
        try:
            host, port = self._parse_url(url)
            ip = socket.gethostbyname(host)
        except Exception:
            return url, MAX_LATENCY

        start_time = time.time()

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=self.timeout
            )
            end_time = time.time()
            latency = (end_time - start_time) * 1000

            writer.close()
            await writer.wait_closed()
            return url, round(latency, 2)
        except Exception:
            return url, MAX_LATENCY

    # --- v2: HTTP Download Test (by_content) ---

    def _build_download_url(self, mirror_url):
        """Construct download URL for pip package from mirror."""
        parsed_url = urlparse(mirror_url)
        host = parsed_url.hostname
        if not host:
            raise ValueError("Invalid mirror URL: {}".format(mirror_url))

        # Remove trailing slash and add /packages/ prefix
        base_url = mirror_url.rstrip("/")

        # Build full download URL
        download_url = urljoin(base_url + "/../", TEST_PACKAGE_PATH)

        return download_url

    def _test_connection_by_content_sync(self, mirror_url):
        """Test download speed for a single mirror synchronously (v2)."""
        try:
            download_url = self._build_download_url(mirror_url)
            speeds = []

            for attempt in range(TEST_COUNT):
                try:
                    start_time = time.time()

                    request = Request(download_url)
                    request.add_header("User-Agent", "pip-fc/1.0")

                    response = urlopen(request, timeout=self.timeout)

                    # Read only first `TEST_FILE_SIZE`
                    data = response.read(TEST_FILE_SIZE)

                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    if elapsed_time > 0:
                        speed = (len(data) / 1024.0) / elapsed_time  # KB/s
                        speeds.append(speed)
                    else:
                        speeds.append(float("inf"))

                except Exception:
                    speeds.append(0)

            if speeds:
                avg_speed = sum(speeds) / len(speeds)
                return mirror_url, round(avg_speed, 2)
            return mirror_url, 0
        except Exception:
            return mirror_url, 0

    async def _test_connection_by_content_async(self, mirror_url):
        """
        Test download speed for a single mirror using low-level asyncio streams.
        This implementation avoids third-party dependencies like aiohttp.
        """
        url = urlparse(self._build_download_url(mirror_url))
        host = url.hostname
        port = url.port or (443 if url.scheme == "https" else 80)
        path = url.path or "/"

        speeds = []

        for _ in range(TEST_COUNT):
            reader, writer = None, None
            try:
                start_time = time.perf_counter()

                # Establish an asynchronous TCP connection
                # ssl=True triggers the SSL/TLS handshake for HTTPS URLs
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port, ssl=(url.scheme == "https")),
                    timeout=self.timeout
                )

                # Construct a minimal HTTP GET request
                # Connection: close ensures the server closes the socket after sending data
                request = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: pip-fc/1.0\r\n"
                    f"Connection: close\r\n\r\n"
                )

                writer.write(request.encode())
                await writer.drain()

                # 先读取头部，检查状态码
                # 注意：这里为了性能，简单读取第一行即可
                line = await asyncio.wait_for(reader.readline(), timeout=self.timeout)
                status_line = line.decode("latin-1").strip()

                # 如果不是 200 OK，视为失败 (避免将 301/302 页面当作极速下载)
                if " 200 " not in status_line:
                    writer.close()
                    await writer.wait_closed()
                    speeds.append(0)
                    print(f"  [warning] {mirror_url}: {status_line.strip()}")
                    continue

                # Read up to TEST_FILE_SIZE bytes
                # Note: This includes the HTTP response headers in the size calculation
                data = await asyncio.wait_for(
                    reader.read(TEST_FILE_SIZE),
                    timeout=self.timeout
                )

                elapsed_time = time.perf_counter() - start_time
                if elapsed_time > 0 and len(data) > 0:
                    # Calculate speed in KB/s
                    speed = (len(data) / 1024.0) / elapsed_time
                    speeds.append(speed)
                else:
                    speeds.append(0)

            except Exception as e:
                # Fallback to 0 speed on timeout or connection errors
                speeds.append(0)
            finally:
                # Properly close the stream writer
                if writer:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except Exception:
                        pass

        # Calculate the arithmetic mean of all test attempts
        avg_speed = sum(speeds) / len(speeds) if speeds else 0
        return mirror_url, round(avg_speed, 2)

    def _test_sync(self, url):
        """Dispatch to appropriate sync test method based on mode."""
        if self.test_method == "by_tcp":
            return self._test_connection_by_tcp_sync(url)
        else:  # by_content
            return self._test_connection_by_content_sync(url)

    async def _test_async(self, url):
        """Dispatch to appropriate async test method based on mode."""
        if self.test_method == "by_tcp":
            return await self._test_connection_by_tcp_async(url)
        else:  # by_content
            return await self._test_connection_by_content_async(url)

    # --- Execution Logic ---

    async def _run_async(self):
        """Run all async test tasks concurrently."""
        tasks = [self._test_async(url) for url in self.urls]
        return await asyncio.gather(*tasks)

    # --- Main Execution Logic ---

    def compare_connection_speeds(self, test_time=2):
        """ Choose execution mode based on Python version. &
            Compare speeds of all mirrors using selected test mode.
        """

        if self.mode == "unsupported":
            print(
                "Error: Python version is too old (< 2.7 or missing 'futures' dependency for 2.7). Cannot proceed."
            )
            return

        mode_name = "TCP connection (v1)" if self.test_method == "by_tcp" else "HTTP download (v2)"
        if self.test_method == "by_content":
            print("--- Starting {} for speedtest ({} bytes, {} times average) ---".format(
                mode_name, TEST_FILE_SIZE, TEST_COUNT
            ))
        else:
            print("--- Starting {} test ---".format(mode_name))

        if self.mode == "asyncio":
            # Prefer asyncio
            try:
                # asyncio.run exists in 3.7+, but this branch will be enabled only for >=3.8
                for _ in range(test_time):
                    self.results += asyncio.run(self._run_async())
            except Exception as e:
                print(f"Asyncio execution failed: {e}. Falling back to Threading.")
                for _ in range(test_time):
                    self.results += self._run_sync_executor()

        elif self.mode.startswith("threading"):
            # Use ThreadPoolExecutor (compatible with 2.7 and 3.x)
            for _ in range(test_time):
                self.results += self._run_sync_executor()

        self._report_results()

    def _run_sync_executor(self):
        """Run sync tests using ThreadPoolExecutor."""
        max_workers = min(32, len(self.urls))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._test_sync, url) for url in self.urls]
            return [future.result() for future in futures]

    def _report_results(self):
        """Report test results and determine the fastest mirror."""
        # Group results by URL
        url_values = {}
        for url, value in self.results:
            if self.test_method == "by_tcp":
                # For TCP mode: lower latency is better
                if value != MAX_LATENCY:
                    if url not in url_values:
                        url_values[url] = []
                    url_values[url].append(value)
            else:
                # For content mode: higher speed is better
                if value > 0:
                    if url not in url_values:
                        url_values[url] = []
                    url_values[url].append(value)

        # Calculate average values and sort
        averages = []
        for url, values in url_values.items():
            avg_value = sum(values) / len(values)
            averages.append((url, avg_value))

        # Sort based on mode
        if self.test_method == "by_tcp":
            # Lower latency is better
            averages.sort(key=lambda x: x[1])
        else:
            # Higher speed is better
            averages.sort(key=lambda x: x[1], reverse=True)

        # Print results
        if self.test_method == "by_tcp":
            print("\nMirror TCP Connection Test Results (sorted by latency):")
            print("-" * 40)
            print("{:<10} {:<60}".format("Latency (ms)", "URL"))
            print("-" * 40)

            for url, avg_value in averages:
                print("{:<10.2f} {}".format(avg_value, url))

            if averages:
                fastest_url, fastest_value = averages[0]
                print("-" * 40)
                print("\n*** Fastest mirror is: {} (latency: {:.2f}ms)".format(fastest_url, fastest_value))
                self.__fastest_url = fastest_url
            else:
                print("\nNo mirror was successfully tested.")
        else:
            print("\nMirror HTTP Download Test Results (sorted by speed):")
            print("-" * 40)
            print("{:<15} {:<60}".format("Speed ({})".format(DOWNLOAD_SPEED_UNIT), "URL"))
            print("-" * 40)

            for url, avg_value in averages:
                print("{:<15.2f} {}".format(avg_value, url))

            if averages:
                fastest_url, fastest_value = averages[0]
                print("-" * 40)
                print("\n*** Fastest mirror is: {} (speed: {:.2f} {})".format(
                    fastest_url, fastest_value, DOWNLOAD_SPEED_UNIT
                ))
                self.__fastest_url = fastest_url
            else:
                print("\nNo mirror was successfully tested.")


def set_global_pip_mirror(mirror_url, backup_mirror_url=None):
    """Set the global pip index-url mirror."""
    try:
        # Set primary mirror
        subprocess.check_call([sys.executable, "-m", "pip", "config", "set", "global.index-url", mirror_url])
        print(f"[pip global] Successfully set pip mirror to: {mirror_url}")

        # Set extra-index-url if provided
        if backup_mirror_url:
            for url in backup_mirror_url:
                subprocess.check_call([sys.executable, "-m", "pip", "config", "set", "global.extra-index-url", url])
            print("[pip global] Successfully set pip extra-index-url (backup mirror) to: {backup_mirror_url}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while setting pip mirror: {e}")
        return False
    return True


def reset_pip_mirror():
    """Reset pip configuration to default settings."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "config", "unset", "global.index-url"])
        subprocess.check_call([sys.executable, "-m", "pip", "config", "unset", "global.extra-index-url"])
        print("pip configuration has been reset to the default settings.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while resetting pip configuration: {e}")
        return False
    return True


def _input_with_timeout(prompt, timeout=5):
    """Prompts user for input with a timeout."""
    from queue import Queue, Empty
    from threading import Thread

    print(prompt)
    result_queue = Queue()

    def get_input():
        user_input = input()
        result_queue.put(user_input)

    # Start the input thread
    input_thread = Thread(target=get_input)
    input_thread.daemon = True  # Ensure it won't block program exit
    input_thread.start()

    # Wait for the input or timeout
    try:
        return result_queue.get(timeout=timeout)
    except Empty:
        print("\nTimeout reached! No input received.")
        return None


def core_main(auto_yes=False, test_mode="by_content"):
    if CONCURRENCY_MODE == "threading_py2" and "futures" not in sys.modules:
        print(
            "Warning: Running on Python 2.7. "
            "Please ensure that the 'futures' library is installed using `pip install futures`."
        )

    tester = MirrorTester(urls=ALL_MIRRORS, test_mode=test_mode)
    tester.compare_connection_speeds()

    print("\n{}\n".format("= " * 20))

    # Determine whether to skip confirmation based on command-line arguments
    if auto_yes:
        inp = "y"
    else:
        inp = _input_with_timeout("Do you want to set the fastest mirror as the global pip mirror? (y/n): ")

    if inp and inp.lower() == "y":
        print("Setting the fastest mirror...")
        EXTRA_INDEX_URLS.append(DEFAULT_INDEX_URL)
        set_global_pip_mirror(
            mirror_url=tester.fastest_url,
            backup_mirror_url=EXTRA_INDEX_URLS
        )
    else:
        print("Skipping mirror setup.")
        sys.exit(0)


def entry_point():
    parser = argparse.ArgumentParser(description="A tool to test mirror sources and configure pip.")
    parser.add_argument(
        "--reset", action="store_true",
        help="Reset pip configuration to default settings."
    )

    # Add -y/–y switch to automatically confirm
    parser.add_argument(
        "-y", "--y", action="store_true",
        help="Automatically confirm setting the fastest mirror."
    )

    parser.add_argument(
        "--test-mode", choices=["by_tcp", "by_content"], default="by_content",
        help="Testing mode: 'by_tcp' for v1 (TCP connection) or 'by_content' for v2 (HTTP download, default)."
    )

    parser.add_argument(
        "--add-nvidia", action="store_true",
        help="(Alpha) Add nvidia mirror for rapids.ai"
    )

    # Paddle wheel
    parser.add_argument(
        "--add-paddle-cpu", action="store_true",
        help="Add PaddlePaddle CPU wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-cu118", action="store_true",
        help="Add PaddlePaddle CUDA 11.8 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-cu126", action="store_true",
        help="Add PaddlePaddle CUDA 12.6 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-cu129", action="store_true",
        help="Add PaddlePaddle CUDA 12.9 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-fastdeploy-80-90", action="store_true",
        help="Add Paddle FastDeploy SM80/90 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-fastdeploy-86-89", action="store_true",
        help="Add Paddle FastDeploy SM86/89 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-gcu", action="store_true",
        help="Add Paddle GCU wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-paddle-npu", action="store_true",
        help="Add Paddle NPU wheel repo as extra-index."
    )

    # PyTorch wheel
    parser.add_argument(
        "--add-pytorch-cpu", action="store_true",
        help="Add PyTorch CPU wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-cu118", action="store_true",
        help="Add PyTorch CUDA 11.8 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-cu121", action="store_true",
        help="Add PyTorch CUDA 12.1 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-cu124", action="store_true",
        help="Add PyTorch CUDA 12.4 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-cu126", action="store_true",
        help="Add PyTorch CUDA 12.6 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-rocm60", action="store_true",
        help="Add PyTorch ROCm 6.0 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-rocm61", action="store_true",
        help="Add PyTorch ROCm 6.1 wheel repo as extra-index."
    )
    parser.add_argument(
        "--add-pytorch-rocm62", action="store_true",
        help="Add PyTorch ROCm 6.2 wheel repo as extra-index."
    )

    # Intel XPU
    parser.add_argument(
        "--add-intel-xpu-us", action="store_true",
        help="Add Intel XPU wheel repo (US) as extra-index."
    )
    parser.add_argument(
        "--add-intel-xpu-cn", action="store_true",
        help="Add Intel XPU wheel repo (CN) as extra-index."
    )

    args = parser.parse_args()

    if args.reset:
        reset_pip_mirror()
        return

    if getattr(args, "add_nvidia", False):
        EXTRA_INDEX_URLS.append("https://pypi.nvidia.com/")

    # Paddle 系
    __base_paddle_mirror = "https://www.paddlepaddle.org.cn/packages/stable"
    if getattr(args, "add_paddle_cpu", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/cpu/")
    if getattr(args, "add_paddle_cu118", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/cu118/")
    if getattr(args, "add_paddle_cu126", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/cu126/")
    if getattr(args, "add_paddle_cu129", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/cu129/")
    if getattr(args, "add_paddle_fastdeploy_80_90", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/fastdeploy-gpu-80_90/")
    if getattr(args, "add_paddle_fastdeploy_86_89", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/fastdeploy-gpu-86_89/")
    if getattr(args, "add_paddle_gcu", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/gcu/")
    if getattr(args, "add_paddle_npu", False):
        EXTRA_INDEX_URLS.append(__base_paddle_mirror + "/npu/")

    # PyTorch whl 仓库
    __base_pytorch_mirror = "https://download.pytorch.org/whl"
    if getattr(args, "add_pytorch_cpu", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/cpu")
    if getattr(args, "add_pytorch_cu118", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/cu118")
    if getattr(args, "add_pytorch_cu121", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/cu121")
    if getattr(args, "add_pytorch_cu124", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/cu124")
    if getattr(args, "add_pytorch_cu126", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/cu126")
    if getattr(args, "add_pytorch_rocm60", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/rocm6.0")
    if getattr(args, "add_pytorch_rocm61", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/rocm6.1")
    if getattr(args, "add_pytorch_rocm62", False):
        EXTRA_INDEX_URLS.append(__base_pytorch_mirror + "/rocm6.2")

    # Intel XPU
    __base_intel_mirror = "https://pytorch-extension.intel.com/release-whl/stable"
    if getattr(args, "add_intel_xpu_us", False):
        EXTRA_INDEX_URLS.append(__base_intel_mirror + "/xpu/us/")
    if getattr(args, "add_intel_xpu_cn", False):
        EXTRA_INDEX_URLS.append(__base_intel_mirror + "/xpu/cn/")

    core_main(auto_yes=args.y, test_mode=args.test_mode)


if __name__ == "__main__":
    entry_point()
