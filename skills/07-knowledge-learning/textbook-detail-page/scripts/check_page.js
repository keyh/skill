// 生成后的页面检查：两种宽度 × 三种身份 × 12 个栏目，无报错、无横向溢出、无空块、无 undefined。
// 用法：node check_page.js 详情页.html   （需要 playwright：npm i playwright && npx playwright install chromium）
const { chromium } = require('playwright')
const F=require('path').resolve(process.argv[2])
const MENU = { student: ['guide','data','toc','kg','ability','question','sz','task','cert','res','ai','eval'], teacher: ['tsel','tfit','team','gksz','kg','ability','question','sz','tapp','res','ai','tbasis'], school: ['ssum','spub','sedit','team','sstd','squal','gksz','res','sevid','sout','stech','sbasis'] }
;(async()=>{const b=await chromium.launch()
for (const W of [1200,390]) { const p=await b.newPage({viewport:{width:W,height:900}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(['error','warning'].includes(m.type()))errs.push(m.text())})
 await p.goto('file://'+F); await p.waitForTimeout(600)
 for (const r in MENU) for (const t of MENU[r]) { await p.evaluate(([r,t])=>{setRole(r,t);setTab(t,false)},[r,t]); await p.waitForTimeout(100)
   const ov = await p.evaluate(()=>document.documentElement.scrollWidth - innerWidth); if (ov>1) errs.push(`overflow ${r}/${t} ${ov}`)
   const empty = await p.evaluate(()=>[...document.querySelectorAll('#content .block')].filter(e=>e.textContent.trim().length<10).length); if (empty) errs.push(`empty block ${r}/${t}`)
   const bad = await p.evaluate(()=>/undefined|NaN|\[object/.test(document.querySelector('#content').innerText)); if (bad) errs.push(`undefined/NaN ${r}/${t}`) }
 console.log(W, errs.length?'FAIL':'OK', JSON.stringify(errs)) }
await b.close()})()
