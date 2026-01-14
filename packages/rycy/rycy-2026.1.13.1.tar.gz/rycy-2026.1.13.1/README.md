# 锐色(rycy)

锐色(rycy) 是一款 HSB 拾色器，只有14种色相(彩度)，分别是：红色(Red)，橙色(Orange)，金色(Gold)，黄色(Yellow)，黄绿(Chartreuse)，春绿(Spring-Greens)，绿色(Green)，青绿(Viridity)，青色(Cyan)，天蓝(Skyblue)，蓝色(Blue)，蓝紫(Bluish-Violet)，紫色(Violet)，紫红(Magenta)。

每种色相只有5%、10%、20%三种浓度和亮度步长，只要确定一种颜色主题，就可以轻松选择需要的颜色，不像传统的拾色器那样密密麻麻的颜色布局导致选择颜色相对困难。

PS: 5%步长按钮在点击时可以在1%、2%、5%进行切换，方便在网页样式设计时选择浅淡的背景色。

## 基本操作

依赖库 pip install PyQt5

PyQt5 需要图形显示相关的系统库，安装所有可能的图形依赖：apt install -y libgl1-mesa-glx libglu1-mesa libxrender1 libxext6 libx11-6 libglib2.0-0 libxcb-* libx11-xcb-dev libxkbcommon-x11-0 xvfb mesa-utils

快捷键：

| 快捷键 | 功能 |
|--------|------|
| `A` (连按3次) | 切换快捷键模式 |
| `1` ~ `7`, `Q` ~ `U` | 选择色相 |
| `D` / `F` / `G` | 步长 5% / 10% / 20% |
| `B` / `N` | S- / B+ |
| `C` / `V` | 复制主色 / 辅色 |
| `X` | 切换复制格式 |
| `H` | 显示帮助 |
| `M` | 最小化窗口 (点击右上角同效) |
| `Esc` | 退出程序 |

## 联系信息

- **更多内容**: 请前往 [锐码官网](http://rymaa.cn) 查阅
- **Pypi 源包仓库**: [https://pypi.org/project/rycy](https://pypi.org/project/rycy)
- **Gitee 源码仓库**: [https://gitee.com/rybby/rycy](https://gitee.com/rybby/rycy)
- **作者**: 锐白
- **主页**: [rybby.cn](http://rybby.cn), [ry.rymaa.cn](http://ry.rymaa.cn)
- **邮箱**: rybby@163.com

## 许可证信息

### 主要许可证

**版权所有 2025 锐码[rymaa.cn](http://rymaa.cn) - rybby@163.com**

本软件采用 GPL v3 开源许可证。使用PyQt5库 (Riverbank Computing, GPL v3)。本程序为自由软件，在自由软件基金会发布的GNU通用公共许可证（第3版或更新版本）的条款下分发。详情请见 <https://www.gnu.org/licenses/gpl-3.0.html> 或应用目录里的 LICENSE 文件。

#### Python 库许可证

| 模块 | 许可证 | 备注 |
|:---:|:---:|:---:|
| os | PSF License | Python标准库 |
| sys | PSF License | Python标准库 |
| argparse | PSF License | Python标准库 |
| subprocess | PSF License | Python标准库 |
| pathlib | PSF License | Python标准库 |
| PyQt5 | GPL v3 / 商业许可 | Qt框架Python绑定 |

## 许可证兼容性

所有这些许可证都是**开源友好**且**商业友好**的：

### 共同特点：
- ✅ 允许商业使用
- ✅ 允许修改
- ✅ 允许分发

### 主要要求：
- 📝 保留原始版权声明
- 📝 在分发时包含许可证文本

## 实际使用建议

- **合规使用**：所有这些模块都可以在商业项目中使用
- **无需担心**：Python 标准库的许可证设计就是为了方便开发者
- **建议做法**：在您的项目 LICENSE 文件中 或 README.md 文件中提及使用了 Python 标准库

## 技术支持

如有问题或建议，请通过以下方式联系：
- 邮箱: rybby@163.com
- 官网: 锐码[rymaa.cn](http://rymaa.cn)

---

*版权所有 2025 锐码[rymaa.cn](http://rymaa.cn)*