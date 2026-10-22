const fs = require('fs')
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, HeadingLevel, BorderStyle } = require('docx')
const log = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))
const names = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'))
const F = 'SimSun'
const t = (s, o = {}) => new TextRun({ text: s, font: F, size: o.size || 21, bold: o.bold, color: o.color })
const P = (s, o = {}) => new Paragraph({ children: [t(s, o)], spacing: { after: 120, line: 320 }, alignment: o.align })
const border = { style: BorderStyle.SINGLE, size: 4, color: 'B7C3D3' }
const borders = { top: border, bottom: border, left: border, right: border }
const W = [600, 2600, 1500, 2200, 4126]
const cell = (s, i, head) => new TableCell({ width: { size: W[i], type: WidthType.DXA }, borders, shading: head ? { type: ShadingType.CLEAR, fill: 'EAF0F8', color: 'auto' } : undefined, margins: { top: 60, bottom: 60, left: 90, right: 90 }, children: [new Paragraph({ children: [t(s, { size: 18, bold: head })] })] })
const fileOf = s => { const m = s.match(/^P(\d+)/); return m ? names[m[1]].replace(/\.docx$/, '') : s }
const order = { '错字/体例': 0, '体例统一': 1, '内容补写（待作者确认）': 2 }
const rows = log.slice().sort((a, b) => (order[a[0]] - order[b[0]]) || (parseInt(a[1].slice(1)) - parseInt(b[1].slice(1))))
const table = new Table({ width: { size: W.reduce((a, b) => a + b), type: WidthType.DXA }, columnWidths: W, rows: [
  new TableRow({ tableHeader: true, children: ['序号', '文件 / 位置', '类型', '修改', '说明'].map((s, i) => cell(s, i, true)) }),
  ...rows.map((r, k) => new TableRow({ children: [String(k + 1), fileOf(r[1]) + (r[1].includes('任务') ? ' · ' + r[1].split(' ')[1] : ''), r[0], r[0].startsWith('内容') ? '赛证直通开头补一句对接说明' : r[2], r[0].startsWith('内容') ? '补写：' + r[3] : (r[3] || '')].map((s, i) => cell(s, i)) }))
] })
const H = s => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(s, { size: 26, bold: true })], spacing: { before: 240, after: 120 } })
const B = s => new Paragraph({ children: [t('· ' + s)], spacing: { after: 80, line: 320 }, indent: { left: 240 } })
const touched = new Set(log.map(r => parseInt(r[1].slice(1))))
const unchanged = Array.from({ length: 16 }, (_, i) => i + 1).filter(n => !touched.has(n)).map(n => String(n).padStart(2, '0'))
const nInhalt = log.filter(r => r[0].startsWith('内容')).length
const doc = new Document({ sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1200, bottom: 1200, left: 1000, right: 1000 } } }, children: [
  new Paragraph({ alignment: AlignmentType.CENTER, children: [t('《老年疾病照护》二稿修订清单', { size: 32, bold: true })], spacing: { after: 80 } }),
  P('与数字教材详情页（知识图谱 · 能力图谱 · 岗课赛证）同步　2026-10-10', { size: 19, color: '607185', align: AlignmentType.CENTER }),
  H('一、修订方式'),
  B('全部修改在 Word 修订模式下完成（修订者：Claude），每处附批注说明理由；原文未做任何不留痕的改动。'),
  B(`体例统一与错字共 ${log.length - nInhalt} 项，属于格式和明显差错，建议直接接受。`),
  B(`内容补写共 ${nInhalt} 处，均为“赛证直通”开头补写的一句对接说明，参照本书同类任务写法拟定，请作者核实对接的赛项、证书等级与考核模块后接受或修改。`),
  B(`项目${unchanged.join('、')} 无修改，原样附上；项目09 原为 .doc 格式，已转换为 .docx 后修订。`),
  B('项目10、16 原稿中已有作者的修订痕迹与批注，本次未做处理，请一并审阅。'),
  H('二、修订明细'),
  table,
  H('三、未在稿件中修改、需作者或出版社确认的事项'),
  B('赛项名称写法不统一：稿件中同时出现“全国职业院校技能大赛养老照护赛项”“职业院校技能大赛健康养老照护赛项”“世界职业院校技能大赛健康养老照护赛项”，建议按当年赛项规程统一核定。'),
  B('多个任务写有“以下题目选自大赛真题及参考题库”，请核实题目来源与授权。'),
  B('项目二任务3、任务4 的评价表没有素养类评价维度（如综合素养、职业素养），其余任务均有，建议补齐。'),
  B('课程能力图谱的企业参与佐证（企业调研与跟岗记录、典型工作任务工作坊纪要、企业专家签字确认）与年度复盘修订记录，不在稿件内，需出版社另行补充，供院校审选使用。'),
  H('四、对数字教材详情页的影响'),
  B('详情页的五级结构数据已按修订稿重新抽取：66 个任务五级结构全部完整，流程 305 步、技能点 778 条、知识点 277 个。'),
  B(`${nInhalt} 处补写的对接说明在详情页上标为“修订稿补写 · 待作者确认”，不计入赛证对接率；作者确认后重新导入即可计入。`)
] }] })
Packer.toBuffer(doc).then(b => fs.writeFileSync(process.argv[4], b))
