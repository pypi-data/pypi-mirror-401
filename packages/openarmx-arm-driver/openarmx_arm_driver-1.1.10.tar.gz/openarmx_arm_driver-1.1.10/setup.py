from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist
import subprocess
import os
import sys
import glob


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(self):
        return True


def compile_so_files(script_dir):
    """编译 .so 文件的通用函数"""
    build_so_script = os.path.join(script_dir, 'build_so.py')
    lib_dir = os.path.join(script_dir, 'src', 'openarmx_arm_driver', '_lib')

    # 检查是否已经有 .so 文件
    so_files = glob.glob(os.path.join(lib_dir, '*.so'))

    if so_files:
        print("\n" + "=" * 60)
        print(f"✓ 检测到已有 {len(so_files)} 个 .so 文件，跳过编译")
        print("=" * 60 + "\n")
        return True

    if not os.path.exists(build_so_script):
        print(f"\n警告: 未找到 build_so.py")
        print(f"查找路径: {build_so_script}\n")
        return False

    print("\n" + "=" * 60)
    print("正在编译 .so 文件...")
    print("=" * 60 + "\n")

    try:
        # 调用 build_so.py --auto（非交互式模式）
        print(f"执行: {sys.executable} {build_so_script} --auto\n")
        result = subprocess.run(
            [sys.executable, build_so_script, '--auto'],
            cwd=script_dir,
            check=True,
            capture_output=False
        )
        print("\n" + "=" * 60)
        print("✓ .so 文件编译完成")
        print("=" * 60 + "\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n错误: build_so.py 执行失败 (退出码: {e.returncode})")
        print("提示: 请确保已安装 Cython: pip install Cython")
        return False
    except Exception as e:
        print(f"\n错误: 执行 build_so.py 时发生异常: {e}")
        return False


class sdist(_sdist):
    """自定义 sdist，在构建源码包之前先编译 .so 文件"""

    def run(self):
        """在构建 sdist 之前自动编译 .so 文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))

        print("\n" + "=" * 60)
        print("【步骤 1/2】构建 sdist 前：编译 .so 文件")
        print("=" * 60)

        if not compile_so_files(script_dir):
            print("\n错误: .so 文件编译失败，无法继续构建 sdist")
            sys.exit(1)

        print("=" * 60)
        print("【步骤 2/2】构建 sdist（tar.gz）")
        print("=" * 60 + "\n")

        # 调用原始的 run 方法构建 sdist
        _sdist.run(self)


class build_py(_build_py):
    """自定义 build_py，排除 _lib 中的 .py 源码文件"""

    def find_package_modules(self, package, package_dir):
        """重写此方法，过滤掉 _lib 中的 .py 文件"""
        modules = _build_py.find_package_modules(self, package, package_dir)

        # 过滤掉 openarmx_arm_driver._lib 中的 .py 文件（保留 __init__.py）
        filtered_modules = []
        for (pkg, module, module_file) in modules:
            # 如果是 _lib 包中的模块
            if pkg == 'openarmx_arm_driver._lib':
                # 只保留 __init__
                if module == '__init__':
                    filtered_modules.append((pkg, module, module_file))
                # 其他 .py 文件都不包含
            else:
                # 其他包的所有模块都保留
                filtered_modules.append((pkg, module, module_file))

        return filtered_modules


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # 自动检测架构并设置正确的平台标签
            self.plat_name_supplied = True

            # 通过检查 .so 文件名来确定架构
            lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'src', 'openarmx_arm_driver', '_lib')
            so_files = glob.glob(os.path.join(lib_dir, '*.so'))

            detected_arch = None
            if so_files:
                # 检查第一个 .so 文件的架构
                so_name = os.path.basename(so_files[0])
                if 'aarch64' in so_name or 'arm64' in so_name:
                    detected_arch = 'manylinux_2_17_aarch64'
                elif 'x86_64' in so_name or 'amd64' in so_name:
                    detected_arch = 'manylinux_2_17_x86_64'

            # 如果无法从 .so 文件检测，使用系统架构
            if not detected_arch:
                import platform
                machine = platform.machine().lower()
                if machine in ['aarch64', 'arm64']:
                    detected_arch = 'manylinux_2_17_aarch64'
                elif machine in ['x86_64', 'amd64']:
                    detected_arch = 'manylinux_2_17_x86_64'
                else:
                    detected_arch = 'manylinux_2_17_x86_64'  # 默认

            self.plat_name = detected_arch
            print(f"\n检测到架构: {detected_arch}\n")

        def run(self):
            """在构建 wheel 之前检查/编译 .so 文件"""
            script_dir = os.path.dirname(os.path.abspath(__file__))

            print("\n" + "=" * 60)
            print("构建 wheel 前：检查 .so 文件")
            print("=" * 60)

            # 尝试编译（如果已有 .so 会跳过）
            compile_so_files(script_dir)

            print("=" * 60)
            print("构建 wheel（.whl）")
            print("=" * 60 + "\n")

            # 调用原始的 run 方法构建 wheel
            _bdist_wheel.run(self)

    cmdclass = {'sdist': sdist, 'bdist_wheel': bdist_wheel, 'build_py': build_py}
except ImportError:
    cmdclass = {'sdist': sdist, 'build_py': build_py}


setup(
    distclass=BinaryDistribution,
    cmdclass=cmdclass,
)
