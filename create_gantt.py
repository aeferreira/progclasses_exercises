"""
GANTT Chart with Matplotlib
Sukhbinder
Inspired from
<div class="embed-theclowersgroup"><blockquote class="wp-embedded-content"><a href="http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/">Gantt Charts in Matplotlib</a></blockquote><script type="text/javascript"><!--//--><![CDATA[//><!--        !function(a,b){"use strict";function c(){if(!e){e=!0;var a,c,d,f,g=-1!==navigator.appVersion.indexOf("MSIE 10"),h=!!navigator.userAgent.match(/Trident.*rv:11./),i=b.querySelectorAll("iframe.wp-embedded-content");for(c=0;c<i.length;c++)if(d=i[c],!d.getAttribute("data-secret")){if(f=Math.random().toString(36).substr(2,10),d.src+="#?secret="+f,d.setAttribute("data-secret",f),g||h)a=d.cloneNode(!0),a.removeAttribute("security"),d.parentNode.replaceChild(a,d)}else;}}var d=!1,e=!1;if(b.querySelector)if(a.addEventListener)d=!0;if(a.wp=a.wp||{},!a.wp.receiveEmbedMessage)if(a.wp.receiveEmbedMessage=function(c){var d=c.data;if(d.secret||d.message||d.value)if(!/[^a-zA-Z0-9]/.test(d.secret)){var e,f,g,h,i,j=b.querySelectorAll('iframe[data-secret="'+d.secret+'"]'),k=b.querySelectorAll('blockquote[data-secret="'+d.secret+'"]');for(e=0;e<k.length;e++)k[e].style.display="none";for(e=0;e<j.length;e++)if(f=j[e],c.source===f.contentWindow){if(f.removeAttribute("style"),"height"===d.message){if(g=parseInt(d.value,10),g>1e3)g=1e3;else if(200>~~g)g=200;f.height=g}if("link"===d.message)if(h=b.createElement("a"),i=b.createElement("a"),h.href=f.getAttribute("src"),i.href=d.value,i.host===h.host)if(b.activeElement===f)a.top.location.href=d.value}else;}},d)a.addEventListener("message",a.wp.receiveEmbedMessage,!1),b.addEventListener("DOMContentLoaded",c,!1),a.addEventListener("load",c,!1)}(window,document);//--><!]]></script><iframe sandbox="allow-scripts" security="restricted" src="http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/embed/" title="“Gantt Charts in Matplotlib” — The Clowers Group" marginwidth="0" marginheight="0" scrolling="no" class="wp-embedded-content" width="600" height="338" frameborder="0"></iframe></div>
"""
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, WEEKLY, MONTHLY, DateFormatter, rrulewrapper, RRuleLocator 
import numpy as np

from matplotlib.cm import get_cmap
from collections import OrderedDict

def _create_date(datetxt):
    """Creates the date"""
    day, month, year=datetxt.split('-')
    date = dt.datetime(int(year), int(month), int(day))
    return date2num(date) 

def _read_tasks(filename):
    tasks = OrderedDict()
    
    with open(filename) as f:
        lines = f.read().splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith('#') or len(line) == 0:
            continue
        ylabel, startdate, enddate, *rest = [p.strip() for p in line.split('\t')]
        tasks[ylabel] = [_create_date(startdate),_create_date(enddate)]

    return tasks

def CreateGanttChart(fname):
    """Create Gantt charts with matplotlib from a TSV file `fname`.""" 

    tasks = _read_tasks(fname)
             
    n = len(tasks)
    cmap = get_cmap('Dark2', 8).colors
    pos = np.arange(0.5, n*0.5+0.5, 0.5)
       
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111)
    
    for i, task in enumerate(tasks):
         start_date, end_date = tasks[task]
         ax.barh((i*0.5) + 0.5, end_date - start_date,
                 left=start_date, height=0.3, align='center',
                 edgecolor='darkgrey', color=cmap[i], alpha=0.8)
    
    ax.set_ylim(bottom=-0.1, top=n*0.5+0.5)
    ylabels = list(tasks)
    plt.yticks(pos, ylabels, fontsize=10)
    #ax.axis('tight')
    
    ax.grid(color = 'lightgrey', linestyle = ':')
    
    ax.xaxis_date()
    rule = rrulewrapper(MONTHLY, interval=1)
    loc = RRuleLocator(rule)
    formatter = DateFormatter("%m-%Y")
    #formatter = DateFormatter("%d-%b")
  
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=30, fontsize=10)
 
    #font = font_manager.FontProperties(size='small')
    #ax.legend(loc=1,prop=font)
    
    plt.subplots_adjust(left=0.2)
    ax.invert_yaxis()
    
    fig.autofmt_xdate()
    
    #plt.savefig('gantt.svg')
    plt.show()
 
if __name__ == '__main__':
    fname = "tasks.txt"
    CreateGanttChart(fname)