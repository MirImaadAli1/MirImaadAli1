"""Outline Roboto text so GitHub image rendering cannot substitute fonts."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

FONT=TTFont(Path(__file__).resolve().parents[1]/'assets/fonts/Roboto.ttf')
GLYPHS=FONT.getGlyphSet()
CMAP=FONT.getBestCmap()
UNITS=FONT['head'].unitsPerEm
CACHE={}
ET.register_namespace('', 'http://www.w3.org/2000/svg')

def outline(svg):
    root=ET.fromstring(svg)
    for element in root.iter():
        if element.tag.rsplit('}',1)[-1]!='text':
            continue
        label=''.join(element.itertext())
        size=float(element.get('font-size','20'))
        x=float(element.get('x','0')); y=float(element.get('y','0'))
        attrs={key:value for key,value in element.attrib.items() if key not in ('x','y','font-size','font-family','font-weight')}
        element.clear(); element.tag='{http://www.w3.org/2000/svg}g'; element.attrib.update(attrs)
        ET.SubElement(element,'{http://www.w3.org/2000/svg}title').text=label
        offset=0
        for char in label:
            if char not in CACHE:
                name=CMAP.get(ord(char),'.notdef'); glyph=GLYPHS[name]
                pen=SVGPathPen(GLYPHS); glyph.draw(pen)
                CACHE[char]=(pen.getCommands(),glyph.width)
            commands,width=CACHE[char]
            if commands:
                ET.SubElement(element,'{http://www.w3.org/2000/svg}path',{'d':commands,'transform':f'translate({x+offset*size/UNITS:.3f} {y}) scale({size/UNITS:.6f} {-size/UNITS:.6f})'})
            offset+=width
    return ET.tostring(root,encoding='unicode')

if __name__=='__main__':
    if len(sys.argv)>1:
        for file in sys.argv[1:]:
            p=Path(file);p.write_text(outline(p.read_text()))
    else:
        print(outline(sys.stdin.read()))
