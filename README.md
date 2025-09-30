# LicensePlateRecommendApp
车管所自选号牌推荐系统

VS Code + Live Server
安装 VS Code
安装 "Live Server" 插件
右键点击 index.html → "Open with Live Server"
3. 重要说明
首次运行：Tesseract.js 会自动下载中文识别模型（约 20-50MB），需要联网
后续运行：模型会被浏览器缓存，可离线使用
识别效果：依赖图片质量和 Tesseract 的能力，可能需要调整识别参数
性能：OCR 过程在浏览器中运行，可能会较慢，尤其在首次加载时
4. 功能特点
✅ 完全前端实现，无需后端
✅ 支持中文车牌识别
✅ 拖拽上传和点击上传
✅ OCR 识别 + 评分分类
✅ 交互式界面，可标记车牌位置
✅ 筛选、排序、搜索功能
这个版本结合了真实的 Tesseract.js OCR 识别引擎和原有的智能推荐系统，实现了您要求的离线车牌识别功能！