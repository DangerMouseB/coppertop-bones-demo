# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# **********************************************************************************************************************


# https://ipycanvas.readthedocs.io/en/latest/installation.html
# conda install -c conda-forge ipycanvas
# jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas

# https://blog.jupyter.org/ipycanvas-a-python-canvas-for-jupyter-bbb51e4777f7
# https://github.com/martinRenou/ipycanvas

#
# with hold_canvas(c):
#     # Perform drawings...


# https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Drawing_text

# x = 10;y = 70; ctx.font = '32px sans-serif'; ctx.textAlign = 'start';
# ctx.textBaseline = "hanging";
# var t = 'Why hello world?';
# var text = ctx.measureText(t);
# asc = text.actualBoundingBoxAscent; desc = text.actualBoundingBoxDescent;
#
# l = text.actualBoundingBoxLeft; r = text.actualBoundingBoxRight;
#
# ctx.fillText(t, x, y); ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(x, y); ctx.moveTo(x+l, y-asc); ctx.lineTo(x+l, y+desc);
# ctx.lineTo(x+r, y+desc); ctx.lineTo(x+r, y-asc); ctx.lineTo(x+l, y-asc); ctx.stroke();
# ctx.font = '18pt sans-serif'; ctx.textAlign = 'start';
# ctx.fillText(asc, 0, y+60);ctx.fillText(desc, 0, y+90);ctx.fillText(asc+desc, 0, y+120);



from ipycanvas import Canvas, RoughCanvas, hold_canvas
from coppertop.pipe import *
from ribs.types import num, tvfloat, index, num, txt
from bones.lang.metatypes import BType

__all__ = [
    'canvas', 'rough', 'fill', 'clear', 'outline', 'style', 'line', 'text', 'save', 'restore', 'clip',
    'relative', 'toFile'
]


def _newCanvas(*args, **kwargs):
    c = Canvas(**kwargs)
    c._t = BType('canvas')
    c._v = c
    return c

def _newRough(*args, **kwargs):
    c = RoughCanvas(**kwargs)
    c._t = BType('rough')
    c._v = c
    return c

canvas = BAtom.ensure('canvas')
canvas.setConstructor(_newCanvas)

# MUSTDO fleshout the rough stuff
rough = BAtom.ensure('rough')
rough.setConstructor(_newRough)

relative = num['canvas.relative'].setCoercer(tvfloat)

@coppertop
def fill(c:canvas+rough, x1, y1, x2, y2) -> canvas+rough:
    x1 -= 1;
    y1 -= 1
    w, h = x2 - x1, y2 - y1
    c.fill_rect(x1, c.height - y1 - h, w, h)
    return c

@coppertop
def fill(c:canvas+rough, x1:index+num, y1:index+num, x2:relative, y2:relative) -> canvas+rough:
    x1 -= 1;
    y1 -= 1
    x2 = x1 + x2
    y2 = y1 + y2
    w, h = x2 - x1, y2 - y1
    c.fill_rect(x1, c.height - y1 - h, w, h)
    return c


@coppertop
def clear(c:canvas+rough, x1, y1, x2, y2) -> canvas+rough:
    x1 -= 1;
    y1 -= 1
    w, h = x2 - x1, y2 - y1
    c.clear_rect(x1, c.height - y1 - h, w, h)
    return c


@coppertop
def outline(c:canvas+rough, x1, y1, x2, y2) -> canvas+rough:
    x1 -= 1;
    y1 -= 1
    w, h = x2 - x1, y2 - y1
    c.stroke_rect(x1, c.height - y1 - h, w, h)
    return c

@coppertop
def outline(c:canvas+rough, x1:index+num, y1:index+num, x2:relative, y2:relative) -> canvas+rough:
    x1 -= 1;
    y1 -= 1
    x2 = x1 + x2
    y2 = y1 + y2
    w, h = x2 - x1, y2 - y1
    c.stroke_rect(x1, c.height - y1 - h, w, h)
    return c


@coppertop
def text(c:canvas+rough, x, y, s:txt) -> canvas+rough:
    x -= 1; y -= 1
    h = 0
    c.fill_text(s, x, c.height - y - h)
    return c


@coppertop
def clip(c:canvas+rough, x1, y1, x2, y2) -> canvas+rough:
    x1 -= 1; y1 -= 1; x2 -= 1; y2 -= 1
    y1 = c.height - y1
    y2 = c.height - y2
    c.move_to(x1, y1)
    c.begin_path()
    c.line_to(x2, y1)
    c.line_to(x2, y2)
    c.line_to(x1, y2)
    c.line_to(x1, y1)
    c.clip()
    return c


@coppertop
def save(c:canvas+rough) -> canvas+rough:
    c.save()
    return c


@coppertop
def restore(c:canvas+rough) -> canvas+rough:
    c.restore()
    return c


@coppertop
def style(c:canvas+rough, **kwargs) -> canvas+rough:
    for k, v in kwargs.items():
        if k == 'fill':
            c.fill_style = v
        elif k == 'stroke':
            c.stroke_style = v
        elif k == 'width':
            c.line_width = v
        elif k == 'alpha':
            c.global_alpha = v
        elif k == 'font':
            # https://www.w3schools.com/tags/canvas_font.asp
            # https://www.w3schools.com/cssref/pr_font_font.asp
            c.font = v
        elif k == 'align':
            c.text_align = v
        elif k == 'baseline':
            c.text_baseline = v
        elif k == 'direction':
            c.direction = v
        else:
            raise TypeError(f'Unknown style type - {k}')
    return c


@coppertop
def line(c:canvas+rough, x1, y1, x2, y2) -> canvas+rough:
    x1 -= 1;
    y1 -= 1;
    x2 -= 1;
    y2 -= 1
    c.stroke_line(x1, c.height - y1, x2, c.height - y2)
    return c


@coppertop
def line(c:canvas+rough, x1:index+num, y1:index+num, x2:relative, y2:relative) -> canvas+rough:
    x1 -= 1;
    y1 -= 1;
    x2 = x1 + x2;
    y2 = y1 + y2
    c.stroke_line(x1, c.height - y1, x2, c.height - y2)
    return c

@coppertop
def toFile(c:canvas+rough, pfn:txt) -> canvas+rough:
    c.to_file(pfn)
    return c



