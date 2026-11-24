# -*- coding: utf-8 -*-
"""生成「片单」项目技术介绍 PPT（16:9 深色主题，重讲述、不贴代码）"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- 主题色 ----------
BG      = RGBColor(0x0E, 0x0E, 0x13)
CARD    = RGBColor(0x1A, 0x1A, 0x23)
CARD2   = RGBColor(0x20, 0x1F, 0x2B)
ACCENT  = RGBColor(0xE5, 0x09, 0x14)
TEXT    = RGBColor(0xF5, 0xF5, 0xF7)
BODY    = RGBColor(0xD2, 0xD2, 0xDA)
MUTED   = RGBColor(0x8A, 0x8F, 0x98)
BORDER  = RGBColor(0x2A, 0x2A, 0x35)
GOLD    = RGBColor(0xFF, 0xD4, 0x3B)

FONT = 'Microsoft YaHei'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def set_font(run, size=None, color=None, bold=None, name=FONT):
    run.font.name = name
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    if bold is not None:
        run.font.bold = bold
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', name)


def new_slide():
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = BG
    return s


def rect(slide, x, y, w, h, fill=CARD, line=BORDER, lw=1.0,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(lw)
    sp.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    return sp


def tx(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
       line_spacing=1.0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        for (t, s, c, b) in runs:
            r = p.add_run()
            r.text = t
            set_font(r, size=s, color=c, bold=b)
    return tb


def slide_title(slide, title, subtitle=None):
    rect(slide, 0.6, 0.55, 0.14, 0.6, fill=ACCENT, line=None, shape=MSO_SHAPE.RECTANGLE)
    tx(slide, 0.92, 0.42, 11.5, 0.9, [[(title, 30, TEXT, True)]])
    if subtitle:
        tx(slide, 0.95, 1.16, 11.5, 0.4, [[(subtitle, 14, MUTED, False)]])
    tx(slide, 0.6, 7.02, 12.1, 0.35, [[('片单 · 项目技术介绍', 10, MUTED, False)]])


def bullet_list(slide, x, y, w, h, items, size=17, gap=16, color=BODY):
    paras = []
    for it in items:
        if isinstance(it, tuple):
            head, rest = it
            paras.append([('▸  ', size, ACCENT, True), (head, size, TEXT, True),
                          (rest, size, color, False)])
        else:
            paras.append([('▸  ', size, ACCENT, True), (it, size, color, False)])
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        p.line_spacing = 1.2
        for (t, s, c, b) in runs:
            r = p.add_run()
            r.text = t
            set_font(r, size=s, color=c, bold=b)
    return tb


def card(slide, x, y, w, h, title, desc, dot_color=ACCENT):
    rect(slide, x, y, w, h, fill=CARD, line=BORDER, lw=1.0)
    rect(slide, x + 0.22, y + 0.24, 0.14, 0.14, fill=dot_color, line=None,
         shape=MSO_SHAPE.OVAL)
    tx(slide, x + 0.48, y + 0.16, w - 0.6, 0.4, [[(title, 17, TEXT, True)]])
    tx(slide, x + 0.25, y + 0.6, w - 0.5, h - 0.7, [[(desc, 12.5, MUTED, False)]],
       line_spacing=1.15)


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ============================================================
# S1 封面
# ============================================================
s = new_slide()
rect(s, 0, 0, 13.333, 0.16, fill=ACCENT, line=None, shape=MSO_SHAPE.RECTANGLE)
rect(s, 0.9, 1.1, 2.6, 0.5, fill=ACCENT, line=None, radius=0.5)
tx(s, 0.9, 1.18, 2.6, 0.4, [[('项目技术介绍', 13, TEXT, True)]], align=PP_ALIGN.CENTER)
tx(s, 0.88, 2.15, 11.5, 1.5, [[('片单', 66, TEXT, True)]])
tx(s, 0.9, 3.35, 11.5, 0.6, [[('一个 Vue 3 电影片单应用', 24, BODY, False)]])
rect(s, 0.95, 4.25, 1.6, 0.06, fill=ACCENT, line=None, shape=MSO_SHAPE.RECTANGLE)
tx(s, 0.9, 4.6, 11.5, 0.5, [[('Vue 3 · Vite · Vue Router · Pinia · axios · ECharts', 15, MUTED, False)]])
tx(s, 0.9, 6.7, 11.5, 0.4, [[('纯前端演示 · 本地 Mock 数据 · 2026', 12, MUTED, False)]])
add_notes(s, '大家好，今天介绍我用 Vue 3 做的一个电影片单应用「片单」。接下来我会先讲清楚这个项目是做什么的、解决了什么问题，再把技术栈逐项展开，说明每一项技术在这个项目里具体起到了什么作用。')

# ============================================================
# S2 项目介绍
# ============================================================
s = new_slide()
slide_title(s, '项目介绍', '这个项目是做什么的')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('一句话：', '一个「找电影、收藏电影」的片单应用，打开就能逛'),
    ('数据来源：', '本地 Mock 模拟了 100 部影片，纯前端即可运行，无需后端'),
    ('使用场景：', '浏览发现好片 → 看详情 → 加入片单 → 回头还能看统计'),
    ('做它的意义：', '把 Vue 3 一整套生态和技术完整串起来，做一次工程实践'),
], size=18, gap=22)
add_notes(s, '先说清楚项目是做什么的。它是一个找电影、收藏电影的片单应用，打开就能逛。数据用本地模拟的一百部影片，不需要后端就能跑起来。典型的使用场景是：先浏览发现好片，点进详情了解信息，喜欢的加进片单，最后还能到统计页看看整体的规律。做它的目的，是把 Vue 3 一整套生态完整串起来，做一次工程实践。')

# ============================================================
# S3 核心功能
# ============================================================
s = new_slide()
slide_title(s, '核心功能', '围绕「找电影、收藏电影」的五块能力')
feats = [
    ('首页', '轮播推荐、热门榜单、全部影片，一进来就能逛', RGBColor(0x39, 0x87, 0xE5)),
    ('搜索', '按片名、导演、演员、类型模糊匹配', RGBColor(0xD9, 0x59, 0x26)),
    ('详情', '完整信息 + 收藏按钮 + 相关推荐', RGBColor(0x19, 0x9E, 0x70)),
    ('片单', '收藏影片，刷新页面数据也不丢', RGBColor(0xC9, 0x85, 0x00)),
    ('统计', 'KPI 卡片 + 四张图表，一眼看懂整体规律', RGBColor(0xD5, 0x51, 0x81)),
]
cx = [0.95, 5.0, 9.05]
cw, ch = 3.3, 1.9
for i, (t, d, c) in enumerate(feats):
    r, col = divmod(i, 3)
    x, y = cx[col], 1.85 + r * 2.15
    card(s, x, y, cw, ch, t, d, dot_color=c)
add_notes(s, '功能一共五块。首页有轮播推荐、热门榜单和全部影片，一进来就能逛；搜索支持按片名、导演、演员、类型模糊匹配；详情页展示完整信息，还能收藏，并按类型推荐相关影片；片单收藏后刷新也不丢；统计页用图表把一百部影片的规律画出来。')

# ============================================================
# S4 效果预览（占位，用户贴截图）
# ============================================================
s = new_slide()
slide_title(s, '效果预览', '实际运行效果')
labels = ['首页', '详情页', '统计看板']
for i, lab in enumerate(labels):
    x = 0.95 + i * 3.9
    rect(s, x, 1.9, 3.5, 4.3, fill=CARD2, line=BORDER, lw=1.2, radius=0.03)
    tx(s, x, 3.8, 3.5, 0.5, [[(lab, 15, MUTED, False)]], align=PP_ALIGN.CENTER)
    tx(s, x, 4.15, 3.5, 0.4, [[('（此处粘贴截图）', 12, RGBColor(0x5A, 0x5A, 0x66), False)]],
       align=PP_ALIGN.CENTER)
add_notes(s, '这里放三张实际运行的截图，分别是首页、详情页和统计看板。也可以现场打开浏览器直接演示一遍，会更直观。')

# ============================================================
# S5 技术栈总览（作为后面逐项展开的提纲）
# ============================================================
s = new_slide()
slide_title(s, '技术栈总览', '每一项各司其职，下面逐项展开')
techs = [
    ('Vue 3', '页面与组件的骨架', RGBColor(0x42, 0xB8, 0x83)),
    ('Vite', '开发与构建工具', RGBColor(0x64, 0x6C, 0xFF)),
    ('Vue Router', '页面路由与跳转', RGBColor(0x42, 0xB8, 0x83)),
    ('Pinia', '收藏状态管理', RGBColor(0xFF, 0xD8, 0x59)),
    ('axios', '数据请求封装', RGBColor(0x5A, 0x29, 0xE4)),
    ('ECharts', '统计图表可视化', RGBColor(0xE4, 0x5A, 0x3A)),
]
for i, (t, d, c) in enumerate(techs):
    r, col = divmod(i, 3)
    x, y = 0.95 + col * 3.9, 1.9 + r * 2.2
    card(s, x, y, 3.5, 1.9, t, d, dot_color=c)
add_notes(s, '先给一张技术栈总览图。六项技术各司其职：Vue 3 是页面和组件的骨架，Vite 负责开发和构建，Vue Router 管页面路由和跳转，Pinia 管收藏状态，axios 负责数据请求，ECharts 负责统计图表。接下来我逐项展开，重点讲每一项在这个项目里具体做了什么。')

# ============================================================
# S6 Vue 3
# ============================================================
s = new_slide()
slide_title(s, 'Vue 3', '项目的骨架与核心')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('骨架：', '所有页面、组件都由 Vue 3 搭建，是整个项目的地基'),
    ('组合式写法：', '把一个功能的逻辑集中写在一起，页面读起来更连贯、更好维护'),
    ('响应式：', '数据一变，界面自动更新，全程不需要手动操作 DOM'),
    ('组件复用：', '海报卡片、图表容器都做成独立组件，被多个页面反复使用'),
], size=18, gap=22)
add_notes(s, 'Vue 3 是项目的核心，所有页面和组件都由它搭建。我重点用了它的两个特性：一是组合式的写法，把一个功能的逻辑集中写在一起，而不是散落各处，读起来更连贯、也更好维护；二是响应式，数据一变界面就自动更新，不用手动操作 DOM。另外把海报卡片、图表容器这些做成了独立组件，在多个页面里反复复用。')

# ============================================================
# S7 Vite
# ============================================================
s = new_slide()
slide_title(s, 'Vite', '开发与构建体验')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('开发提速：', '项目启动几乎秒开，改代码后页面即时热更新，不用刷新'),
    ('构建优化：', '打包时自动按页面拆分、压缩代码，浏览器加载更快'),
    ('工程配置：', '路径别名、插件、代理等都通过它统一管理'),
], size=18, gap=22)
add_notes(s, 'Vite 负责开发和构建。对开发者来说，它的好处很直接：项目启动几乎秒开，改代码后页面即时热更新，不用手动刷新，开发体验很好。打包的时候，它会自动按页面拆分、压缩代码，让浏览器加载更快。还有一些工程配置，比如路径别名，也是通过它统一管理的。')

# ============================================================
# S8 Vue Router
# ============================================================
s = new_slide()
slide_title(s, 'Vue Router', '页面如何组织与跳转')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('页面导航：', '首页、搜索、详情、分类、片单、统计，共 6 个页面 + 404'),
    ('动态路由：', '每个影片、每个分类都有自己的专属地址，可以分享、收藏'),
    ('细节体验：', '切换页面自动回到顶部，浏览器标题随页面更新'),
    ('性能：', '页面按需加载，首屏只加载当前页，速度更快'),
], size=18, gap=22)
add_notes(s, 'Vue Router 负责页面怎么组织、怎么跳转。整个应用六个页面加一个 404，地址和页面一一对应。用动态路由让每个影片、每个分类都有自己的专属地址，可以直接分享或收藏。另外做了两个体验细节：切换页面自动回到顶部、浏览器标题跟着页面变。性能上页面是按需加载的，首屏只加载当前页。')

# ============================================================
# S9 Pinia
# ============================================================
s = new_slide()
slide_title(s, 'Pinia', '收藏数据如何管理')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('集中管理：', '收藏数据统一放在一个仓库里，各页面共享同一份'),
    ('跨页联动：', '首页角标、详情页按钮、片单页内容实时保持一致'),
    ('持久化：', '收藏自动写入浏览器本地存储，刷新页面数据也不丢'),
], size=18, gap=22)
add_notes(s, 'Pinia 负责管理收藏数据。为什么需要它？因为「收藏」这个状态会出现在很多地方：首页的角标数量、详情页的收藏按钮、片单页的列表，它们必须保持一致。把收藏数据统一放在一个仓库里，各页面共享同一份，就能保证它们实时联动。再配合持久化，收藏会自动存进浏览器本地，刷新页面也不丢。')

# ============================================================
# S10 axios
# ============================================================
s = new_slide()
slide_title(s, 'axios', '数据从哪里来')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('统一入口：', '所有请求封装在一个文件里，页面只调用方法、不关心数据来源'),
    ('前后端分层：', '现在读的是本地模拟数据，将来接真实后端只需改一处'),
    ('可维护：', '数据源的切换对页面完全透明，改起来不动页面代码'),
], size=18, gap=22)
add_notes(s, 'axios 负责数据请求。我的做法是把所有请求封装在一个文件里，页面只调用封装好的方法，完全不关心数据是从哪来的。现在读的是本地模拟数据，将来要接真实后端，只需要改这一个文件，所有页面一行都不用动。这就是前后端分层的思路，让数据源的切换对页面完全透明。')

# ============================================================
# S11 ECharts
# ============================================================
s = new_slide()
slide_title(s, 'ECharts', '数据如何可视化')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('统计看板：', 'KPI 卡片 + 柱状图、环形图、面积折线共 4 张图'),
    ('数据洞察：', '一眼看出剧情片最多、2010 年代是产量高峰'),
    ('工程化：', '按需引入控制体积；封装图表容器，统一处理自适应与销毁'),
], size=18, gap=22)
add_notes(s, 'ECharts 负责数据可视化。统计页用 KPI 卡片加四张图，把一百部影片的类型、地区、评分、年代分布画出来。有了图，一些规律一眼就能看出来，比如剧情片数量最多、2010 年代是产量高峰。工程上做了两点：按需引入来控制打包体积，以及封装一个图表容器，统一处理窗口大小变化时的自适应和销毁。')

# ============================================================
# S12 项目结构
# ============================================================
s = new_slide()
slide_title(s, '项目结构', '按职责分层的目录组织')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('分层清晰：', '页面、组件、状态、请求、路由分别放在独立目录里'),
    ('职责单一：', '新增功能时改动范围明确，互不干扰'),
    ('数据独立：', '模拟数据单独放在 public 目录，和代码分离'),
], size=18, gap=22)
add_notes(s, '项目结构上强调分层。页面、组件、状态、请求、路由分别放在独立的目录里，各管各的。这样职责单一，新增一个功能时改动范围很明确，不会互相干扰。模拟数据单独放在 public 目录下，和代码分离，将来换真实数据源也很方便。')

# ============================================================
# S13 技术亮点
# ============================================================
s = new_slide()
slide_title(s, '技术亮点', '几个值得强调的地方')
bullet_list(s, 0.95, 1.95, 11.4, 4.6, [
    ('架构：', '组件化 + 分层，职责清晰、易于维护'),
    ('体验：', '深色主题、响应式布局、切页回顶、标题联动'),
    ('可视化：', '无障碍配色、图表随窗口自适应缩放'),
    ('性能：', '路由懒加载、图表库按需引入'),
], size=18, gap=22)
add_notes(s, '总结几个亮点。架构上，组件化和分层做得很清楚，职责清晰、好维护。体验上，做了深色主题、移动端响应式、切页回顶和标题联动这些细节。可视化上，图表配色按色盲安全的标准来选，并且图表会随窗口大小自适应。性能上，路由做了懒加载、图表库做了按需引入。')

# ============================================================
# S14 总结与展望
# ============================================================
s = new_slide()
rect(s, 0, 0, 13.333, 0.16, fill=ACCENT, line=None, shape=MSO_SHAPE.RECTANGLE)
slide_title(s, '总结与展望', 'Summary')
bullet_list(s, 0.95, 1.95, 11.4, 3.2, [
    ('完整走通：', '从搭建到打包，串起 Vue 3 全家桶的完整开发流程'),
    ('加深理解：', '对组件化、路由、状态管理、数据可视化有了实战认识'),
    ('下一步：', '接真实后端、用户登录、评分短评、部署上线'),
], size=18, gap=20)
tx(s, 0.95, 5.55, 11.4, 1.0, [[('谢谢观看', 34, TEXT, True)]])
add_notes(s, '最后总结。这个项目让我完整走通了 Vue 3 全家桶从搭建到打包的流程，对组件化、路由、状态管理、数据可视化都有了实战层面的认识。后续计划接真实后端、加用户登录和评分功能，再部署上线。我的分享就到这里，谢谢大家。')

out = '片单-项目介绍-v2.pptx'
prs.save(out)
print('saved:', out, '| slides:', len(prs.slides._sldIdLst))
