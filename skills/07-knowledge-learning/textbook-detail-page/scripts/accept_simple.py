"""仅供抽取用：接受全部修订（删除 w:del、展开 w:ins、去掉段落标记修订与批注标记）。"""
import sys, zipfile, re
src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for i in zin.infolist():
    data = zin.read(i.filename)
    if i.filename == 'word/document.xml':
        x = data.decode('utf-8')
        x = re.sub(r'<w:del\b[^>]*/>', '', x)
        x = re.sub(r'<w:del\b[^>]*>.*?</w:del>', '', x, flags=re.S)
        x = re.sub(r'<w:ins\b[^>]*/>', '', x)
        x = re.sub(r'<w:ins\b[^>]*>', '', x)
        x = x.replace('</w:ins>', '')
        data = x.encode('utf-8')
    zout.writestr(i, data)
zout.close()
