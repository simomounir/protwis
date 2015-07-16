

from math import cos, sin, tan, pi, sqrt, pow
import string, time, math, random

def uniqid(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid

class Diagram:
    def create(self, content,sizex,sizey):
        diagram_js = self.diagramJS()
        return "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></script><svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\""+str(sizex)+"\" height=\""+str(sizey)+"\">\n"+content+"</svg>"+diagram_js #width=\"595\" height=\"430\"

    def drawToolTip(self):
        output = """<g id='tool-tip' transform='translate(0,0)' visibility='hidden'>
            <rect x='0' y='-40' width='1' height='25' stroke='black' fill='white' stroke-width='1' />
            <text x='0' y='-23' text-anchor='middle' font-family='Arial' font-size='12' fill='black'></text>
            </g>"""
        
        return output

    #Draws a ring of a helical wheel  
    def DrawResidue(self, x,y,aa,residue_number,label,radius, resclass = '',cfill="white", precolor = False):
        id = residue_number
        idtext = str(id) + 't'
        tfill = 'black'
        #if (isset(_GET['precolor']) && _GET['precolor'] == 'TRUE') precolor = TRUE
        # if (precolor) {
        #     iid = str_replace('.', '_', id)
        #     iidtext = str_replace('.', '_', idtext)
        #     cfill = isset(_SESSION['color_pattern'][iid]) ? _SESSION['color_pattern'][iid] : 'white'
        #     tfill = isset(_SESSION['color_pattern'][iidtext]) ? _SESSION['color_pattern'][iidtext] : 'black'
        # }
        output =  """
            <circle class='{}' cx='{}' cy='{}' r='{}' stroke='black' stroke-width='2' fill='{}' 
            fill-opacity='1' id='id' class='rcircle' onclick='residueColor.setColor(evt);'
            onmouseover='showToolTip({},{},"{}","id");' onmouseout='hideToolTip();'/>
            <text x='{}' y='{}' text-anchor='middle' font-family='helvetica' font-size='16' fill='tfill'
            id='idtext' onclick='residueColor.setColor(evt);' class='rtext {}'
            onmouseover='showToolTip({},{},"{}","id");' onmouseout='hideToolTip();'>{}</text>
            """.format(resclass,x,y,radius,cfill,x,y,label,x,y+6,resclass,x,y,label,aa) #aa
        return output

    def diagramJS(self):
        output = """<script>

                    presetColors = {'D': ['#E60A0A', '#FDFF7B'],'E': ['#E60A0A', '#FDFF7B'],
                                    'K': ['#145AFF', '#FDFF7B'],'R': ['#145AFF', '#FDFF7B'],
                                    'S': ['#A70CC6', '#FDFF7B'],'T': ['#A70CC6', '#FDFF7B'],
                                    'N': ['#A70CC6', '#FDFF7B'],'Q': ['#A70CC6', '#FDFF7B'],
                                    'V': ['#E6E600', '#000000'],'L': ['#E6E600', '#000000'],
                                    'I': ['#E6E600', '#000000'],'A': ['#E6E600', '#000000'],
                                    'M': ['#E6E600', '#000000'],'F': ['#18FF0B', '#000000'],
                                    'Y': ['#18FF0B', '#000000'],'W': ['#0BCF00', '#000000'],
                                    'H': ['#0093DD', '#000000'],'P': ['#CC0099', '#FDFF7B'],
                                    'C': ['#B2B548', '#000000'],'G': ['#FF00F2', '#000000'],
                                    '-': ['#FFFFFF', '#000000']    
                                    };

                    var translateOffset = 0;
                    function showToolTip(x, y, str,rid) {
                        var tipElement = document.getElementById('tool-tip');

                        var rect = tipElement.childNodes[1];
                        var text = tipElement.childNodes[3];

                        while (text.lastChild) {
                            text.removeChild(text.lastChild);
                        }
                        
                        var NS = "http://www.w3.org/2000/svg";


                        //text.textContent =  str;
                            var text_tspan = document.createElementNS(NS, "tspan");


                            rect.setAttribute('height', 25);
                            rect.setAttribute('y', -40);
                            text_tspan.textContent = String(str);
                            text.appendChild(text_tspan);
                        
                        
                        var bbox = text.getBBox();
                        rect.setAttribute('width', bbox.width + 8);
                        rect.setAttribute('x', -bbox.width/2 - 4);

                        var transX = (x <= (bbox.width + 8) / 2) ? (bbox.width + 8) / 2 : x;
                        tipElement.setAttribute('transform', 'translate(' + transX + ',' + (y + translateOffset) + ')');
                        tipElement.setAttribute('visibility', 'visible');
                    }

                    function hideToolTip() {
                        var tipElement = document.getElementById('tool-tip');
                        tipElement.setAttribute('visibility', 'hidden');
                    }

                    function toggleLoop(id,type) {
                        $(id+".long").toggle();
                        $(id+".short").toggle();
                        maxmin();

                        $(id+".long").toggle();
                        $(id+".short").toggle();

                        $(id+".long").fadeToggle();
                        $(id+".short").fadeToggle();
                    }

                    function applyPresentColors() {

                        $("circle").each(function( index ){
                              console.log( index + ": " + $( this ).closest(".rtext").val() );
                              console.log( index + ": " + $( this ).text() );
                            });

                        var textElements = document.getElementsByClassName('rtext');
                        for (var i=0; i<textElements.length; i++) {
                            var text = textElements[i].textContent;
                            var colorText = presetColors[text][1];
                            var colorCircle = presetColors[text][0];
                            textElements[i].setAttribute('fill', colorText);
                            document.getElementById(textElements[i].id.slice(0, textElements[i].id.length-1)).setAttribute('fill', colorCircle);
                        }
                        
                        var loopResidues = document.getElementsByClassName('loop-residue');
                        for (var i=0; i<loopResidues.length; i++) {
                            var text = loopResidues[i].textContent;
                            loopResidues[i].setAttribute('fill', presetColors[text][0]);
                        }

                    };

                    function maxmin() {
                        margin = 50;
                        svgmax = 0;
                        svgmin = 0;
                        count = 0;
                        classmax = ''
                        classmin = ''
                        $('#snake').children('text').each(function () {
                            if ($(this).is(":visible")) {
                                count = count +1;
                                y = parseInt($(this).attr( "y" ));
                                classtext = $(this).attr( "class" );
                                if (y<svgmin) {
                                    svgmin = y; 
                                    classmin = classtext;
                                    }
                                if (y>svgmax) {

                                    classmax = classtext;
                                    svgmax= y; 
                                 }

                            }   
                        });
                        console.log('max '+svgmax+' '+classmax+' min'+svgmin+' '+classmin+' count'+count);
                        
                        var svg = $('#snake').closest('svg')[0];
                        oldheight = $(svg).attr('height');
                       // svg.setAttribute('height', (svgmax-svgmin+margin*2));
                        $(svg)
                        .animate(
                          {"min-height": (svgmax-svgmin+margin*2)},
                          {duration: 500,
                           step: function( top ){
                               this.setAttribute("height", "translate(0,"+Math.round(top)+")");
                             }
                           });

                        console.log('New height:'+ (svgmax-svgmin) +' old height:'+oldheight);
                        console.log("Prev attr"+$('#snake').attr("transform"));
                        //$('#snake').attr("transform", "translate(0," + (-svgmin+margin) + ")");
                        
                        $('#snake')
                        .animate(
                          {"min-height": (-svgmin+margin)},
                          {duration: 500,
                           step: function( top ){
                               this.setAttribute("transform", "translate(0,"+top+")");
                             }
                           });

                        console.log("New attr"+$('#snake').attr("transform"));
                    }

                    $( document ).ready(function() {    
                        var elements = document.getElementsByClassName('long')

                        for (var i = 0; i < elements.length; i++){
                            elements[i].style.display = 'none';
                        }
                        maxmin();
                        //applyPresentColors();
                    });


                    </script>"""
        return output

    def deg2rad(self,degrees):
        radians = pi * degrees / 180
        return radians

    def bezier(self,p0,p1,p2,t):
        #https://en.wikipedia.org/wiki/B%C3%A9zier_curve

        v1x = p1[0]-p0[0]
        v1y = p1[1]-p0[1]

        i1 = [p0[0]+(p1[0]-p0[0])*t,p0[1]+(p1[1]-p0[1])*t]
        i2 = [p1[0]+(p2[0]-p1[0])*t,p1[1]+(p2[1]-p1[1])*t]

        return [i1[0]+(i2[0]-i1[0])*t,i1[1]+(i2[1]-i1[1])*t]

    def bezier_high(self,p0,p1,p2,p3,t):
        #https://en.wikipedia.org/wiki/B%C3%A9zier_curve

        i1 = self.bezier(p0,p1,p2,t)
        i2 = self.bezier(p1,p2,p3,t)

        return [i1[0]+(i2[0]-i1[0])*t,i1[1]+(i2[1]-i1[1])*t]

    def bezier_high2(self,p0,p1,p2,p3,p4,t):
        #https://en.wikipedia.org/wiki/B%C3%A9zier_curve
        #https://www.jasondavies.com/animated-bezier/
        i1 = self.bezier_high(p0,p1,p2,p3,t)
        i2 = self.bezier_high(p1,p2,p3,p4,t)

        return [i1[0]+(i2[0]-i1[0])*t,i1[1]+(i2[1]-i1[1])*t]

    def lengthbezier(self,p0,p1,p2,step,p3=False,p4=False):
        #https://en.wikipedia.org/wiki/B%C3%A9zier_curve

        pos = 0
        length = 0
        p = p0
        while pos <= 1:

            
            if p3==False: 
                xy = self.bezier(p0,p1,p2,pos)
            elif p4==False: 
                xy = self.bezier_high(p0,p1,p2,p3,pos)
            elif p4!=False: 
                xy = self.bezier_high2(p0,p1,p2,p3,p4,pos)

            length += math.sqrt( (xy[0]-p[0])**2 + (xy[1]-p[1])**2 )
            p = xy
            pos += step

        return round(length)

    def wherebezier(self,p0,p1,p2,step,stop,p3=False,p4=False):
        #https://en.wikipedia.org/wiki/B%C3%A9zier_curve

        pos = 0
        length = 0
        p = p0
        xy = [0,0]

        if stop<0:
            if p3==False: 
                stop = self.lengthbezier(p0,p1,p2,step)+stop
            elif p4==False:
                stop = self.lengthbezier(p0,p1,p2,step,p3)+stop
            else:
                stop = self.lengthbezier(p0,p1,p2,step,p3)+stop

        while pos <= 1:

            if length>stop: #stop if it reached the length along the line
                break

            if p3==False: 
                xy = self.bezier(p0,p1,p2,pos)
            elif p4==False:
                xy = self.bezier_high(p0,p1,p2,p3,pos)
            else:
                xy = self.bezier_high2(p0,p1,p2,p3,p4,pos)

            length += math.sqrt( (xy[0]-p[0])**2 + (xy[1]-p[1])**2 )
            p = xy
            pos += step

        return pos,xy


    #find slope and y-intercept of a line through two points
    def LineEquation(self,p1, p2):
        # slope
        m = (p2['y']-p1['y'])/(p2['x']-p1['x'])

        # y-intercept
        b = p1['y'] - m*p1['x']

        # direction
        if p1['y'] >= p2['y'] and p1["x"] > p2["x"]:
            x = -1
            y = -1
        elif p1['y'] > p2['y'] and p1["x"] < p2["x"]:
            x = 1
            y = 1
        elif p1['y'] < p2['y'] and p1["x"] > p2["x"]:
            x = -1
            y = -1
        elif p1['y'] <= p2['y'] and p1["x"] < p2["x"]:
            x = 1
            y = 1

        return {'m':m, 'b':b, 'x':x, 'y':y}

    def MoveAlongLine(self,pixels_to_move,m,perpendicular, xDir=1, yDir=1):
        # perpendicular line
        if perpendicular == True:
            if m != 0:
                m = -1/m
            else:
                return {"x":0, "y":pixels_to_move}
        
        # a^2+b^2=c^2 where a=x and b=mx
        # x^2+mx^2=c^2 (the b of y=mx+b can be omitted as the y-intercept is zero)
        c = pixels_to_move
        x = sqrt( pow(c,2)/(1+pow(m,2)) )
        y = m*x
        
        return {"x":x*xDir, "y":y*yDir}

    #Draws the full backbone representation for one (box) helix

    def DrawBackbone(self,coordinates):

        # box properties
        numSides = 4

        # start at residue position 1
        cur_res = 1   

        # loop through residues and draw backbone
        output = ""
        #for (i=1;i<=count(coordinates);i++) {
        for i in range(1,len(coordinates)+1):
            cur_res = i

            # find next residue 
            next_res = cur_res-1
            if next_res<1:
                next_res = 19
            
            # find prev residue 
            prev_res = cur_res+1;
            if prev_res>len(coordinates):
                prev_res = 2

            # next-in-wheel residue orientation
            wheel_next_res = cur_res-numSides
            if wheel_next_res <= (1-numSides):  # if current res is the last res, next is the first res
                wheel_next_res = len(coordinates)
            elif wheel_next_res < 1:
                wheel_next_res += len(coordinates)-1
            
            # line thickness
            thickness = 6*((i/len(coordinates)/1.2))
            thicknessNext = 6*(((i+1)/len(coordinates)/1.2))
            thicknessPrev = 6*(((i-1)/len(coordinates)/1.2))

            # find residue base points
            cur_points = self.ResiduePoints(cur_res, thickness, coordinates)
            next_points = self.ResiduePoints(next_res, thicknessNext, coordinates)
            prev_points = self.ResiduePoints(prev_res, thicknessPrev, coordinates) 

            # lines
            cur_in = self.LineEquation(cur_points[1], cur_points[2])
            cur_out = self.LineEquation(cur_points[4], cur_points[3])
            next_in = self.LineEquation(next_points[1], next_points[2])
            next_out = self.LineEquation(next_points[4], next_points[3])
            prev_in = self.LineEquation(prev_points[1], prev_points[2])

            # line points
            p1 = cur_points[1];
            p2 = self.LineIntercept(cur_in['m'], cur_in['b'], next_out['m'], next_out['b'])
            p3 = self.LineIntercept(cur_in['m'], cur_in['b'], next_in['m'], next_in['b'])
            p4 = self.LineIntercept(cur_in['m'], cur_in['b'], prev_in['m'], prev_in['b'])
            p5 = self.LineIntercept(cur_out['m'], cur_out['b'], prev_in['m'], prev_in['b'])
            p6 = cur_points[4]

            # shorter line for the last residue
            if i == len(coordinates):
                move_in = self.MoveAlongLine(40,cur_in['m'],False,cur_in['x'],cur_in['y']);
                p4 = {'x':p1['x']+move_in['x'], 'y':p1['y']+move_in['y']}
                p5 = {'x':p6['x']+move_in['x'], 'y':p6['y']+move_in['y']}
            
            # draw line
            points = [p2,p1,p6,p5,p4,p3]
            points_txt = ""
            for coord in points:
                points_txt += str(coord['x'])+","+str(coord['y'])+" "

            # gradient
            gradientId = uniqid()
            angle = 1/tan(self.deg2rad(cur_in['m']))
            output +=  """
                <defs>
                    <linearGradient id='{}' x1='100%' y1='0%' x2='0%' y2='0%' gradientTransform='rotate({})'>
                    <stop offset='0%' stop-color='#00cc00' stop-opacity='1'/>
                    <stop offset='100%' stop-color='#006600' stop-opacity='1'/>
                    </linearGradient>
                </defs>
                """.format(gradientId,angle)

            lineFill = "white"

            # add SVG to output 
            output += "<polyline stroke='black' stroke-width='0.5' points='"+points_txt+"' fill='"+lineFill+"'/>"

        return output; 

    def LineIntercept(self,m1, b1, m2, b2):
        # line intercept
        intercept = {}
        intercept['x'] = (b2-b1)/(m1-m2)
        intercept['y'] = m1*intercept['x']+b1

        return intercept

    #Finds points on both sides of the residue center and the equation of a line to a reference residue
    def ResiduePoints(self, cur_res, thickness, coordinates):
        # FIXME write a general formula
        ref_residues = {
            20 : 2,
            16 : 2,
            12 : 2, # exception
            8 : 17,
            4 : 13,
            19 : 1,
            15 : 1,
            11 : 20,
            7 : 20,
            3 : 16,
            18 : 4,
            14 : 4,
            10 : 19,
            6 : 19,
            2 : 15,
            17 : 3,
            13 : 3,
            9 : 18,
            5 : 18,
            1 : 14}

        ori = {}

        ref_res = ref_residues[cur_res]

        # next-in-wheel residue orientation
        numSides = 4
        wheel_next_res = cur_res-numSides
        if wheel_next_res <= (1-numSides): # if current res is the last res, next is the first res
            wheel_next_res = len(coordinates)
        elif wheel_next_res < 1:
            wheel_next_res += len(coordinates)-1
        
        # point orientation
        if (coordinates[cur_res]['y'] >= coordinates[wheel_next_res]['y'] and coordinates[cur_res]['x'] > 
            coordinates[wheel_next_res]['x']):
            # SW
            ori['x'] = -1
            ori['y'] = -1
        
        elif (coordinates[cur_res]['y'] > coordinates[wheel_next_res]['y'] and coordinates[cur_res]['x'] < 
            coordinates[wheel_next_res]['x']):
            # NW
            ori['x'] = 1
            ori['y'] = 1
        
        elif (coordinates[cur_res]['y'] < coordinates[wheel_next_res]['y'] and coordinates[cur_res]['x'] > 
            coordinates[wheel_next_res]['x']):
            # SE
            ori['x'] = -1
            ori['y'] = -1
        
        elif (coordinates[cur_res]['y'] <= coordinates[wheel_next_res]['y'] and coordinates[cur_res]['x'] < 
            coordinates[wheel_next_res]['x']):
            # NE
            ori['x'] = 1
            ori['y'] = 1
        

        # slope of line from current residue to reference residue
        m = (coordinates[ref_res]['y']-coordinates[cur_res]['y'])/(coordinates[ref_res]['x']-
            coordinates[cur_res]['x'])

        # calculate coordinates of perpendicular line
        per_move = self.MoveAlongLine(thickness/2,m,True); # move thickness/2 pixels along a perpendicular line
            
        # define points
        points = [0];
        points.append({'x':coordinates[cur_res]['x']+per_move['x']*ori['x'], 'y':coordinates[cur_res]['y']+
            per_move['y']*ori['y']})
        points.append({'x':coordinates[ref_res]['x']+per_move['x']*ori['x'], 'y':coordinates[ref_res]['y']+
            per_move['y']*ori['y']})
        points.append({'x':points[2]['x']+per_move['x']*ori['x']*-2, 'y':points[2]['y']+per_move['y']*
            ori['y']*-2})
        points.append({'x':points[1]['x']+per_move['x']*ori['x']*-2, 'y':points[1]['y']+per_move['y']*
            ori['y']*-2})

        return points