#!/bin/bash

set -euo pipefail

trap 'echo "x 错误发生在第 $LINENO 行，命令：$BASH_COMMAND" >&2' ERR

pkg_name="libcdma"
pkg_version="1.0"
orig_tar="${pkg_name}.tar.gz"
source_dir="${pkg_name}-${pkg_version}"

rm -rf "${source_dir}"

echo "安装构建依赖..."
if [ -f "../debian/control" ]; then
    DEP_PACKAGE=$(dpkg-parsechangelog -S Source 2>/dev/null || echo "${pkg_name}")
else
    DEP_PACKAGE="${pkg_name}"
fi

echo "创建源码目录：${source_dir}"
mkdir -p "${source_dir}"
pushd "${source_dir}" > /dev/null

echo "解压源码包到当前目录"
tar -xzf "../${orig_tar}" --strip-components=1

if [ ! -d "debian" ]; then
    echo "首次构建：生成 debian 目录结构"
    dh_make -y -c gpl3 -s -e "your-email@example.com" --createorig
else
    echo "debian/ 目录已存在，跳过 dh_make"
fi

if [ -d "../debian" ]; then
    echo "拷贝自定义 debian 配置"
    rm -f debian/*.ex debian/*.EX
    cp -ar ../debian/* ./debian/
else
    echo "警告：上次目录未找到 debian/ ，将使用当前 debian/ 目录中的配置"
fi

echo "开始构建 deb 包"
dpkg-buildpackage -rfakeroot -us -uc -b
