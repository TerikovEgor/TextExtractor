import re
from pampy import match, REST, _
from datetime import datetime as dt
from cytoolz.curried import map as MAP
import os 

path = os.path.dirname(__file__) + '/src/'
sp = "[\. /]"

l = "{4}"
jan = re.compile(f"янв(?:арь)?{sp}\d{l}")
feb = re.compile(f"фев(?:раль)?{sp}\d{l}")
mar = re.compile(f"март?{sp}\d{l}")
apr = re.compile(f"апр(?:ель)?{sp}\d{l}")
may = re.compile(f"май{sp}\d{l}")
jun = re.compile(f"июнь?{sp}\d{l}")
jul = re.compile(f"июль?{sp}\d{l}")
aug = re.compile(f"авг(?:уст)?{sp}\d{l}")
sep = re.compile(f"сен(?:тябрь)?{sp}\d{l}")
octb = re.compile(f"окт(?:ябрь)?{sp}\d{l}")
nov = re.compile(f"ноя(?:брь)?{sp}\d{l}")
dec = re.compile(f"дек(?:абрь)?{sp}\d{l}")
current = re.compile(f"н(аст)?(оящее)?{sp}вр(.|емя)?")
digits = re.compile("\d{2}[\./]\d{4}")
repl = re.compile(sp)


perSplit = "(?<=\d) ?(?:\-|до|по) ?"
splitReg = re.compile(perSplit)
period = re.compile("[а-я0-9\.]{,10}" + perSplit + "[а-я0-9\.]{,10}")
permarks = ("from", "to")

spb = "[\./ \-]"

phone = re.compile("(\+?[0-9\(][0-9\- \(\)]{6,16}( ?e?xt?\.? ?\d+)?)")
url = re.compile( "((https?://)\w+(:\d+)?[^ ]*)")
email = re.compile("([\w\.\-_]+@[\w\.\-_]+)")
salary = re.compile("\d{5,} ?(RUR|р(убл?)?(я(ми)?|ей|ю)?)?")
birth = re.compile("\d{,3}" + spb + "(\d\d|(янв|фев|мар|апр|ма|июл|июн|авг|сен|окт|ноя|дек)(\.|(т?[ая]?б?р?[ья]?)|уста?)?)" + spb + "(\d{4})")
jobStr = open(path + "job.txt").read()
job = re.compile(jobStr)

def dater(reg,mon,t):
    found = reg.search(t)
    if found:
        return {"date" : dt(int(repl.split(found[0])[1]),mon, 1) }
    else:
        return 0
    
def genericExtractor(reg,t):
    found = reg.search(t)
    if found:
        return found[0]
    else:
        return ""
    
def exPer(s):
    found = period.search(s)
    if found:
        return dict(zip(permarks, MAP(extractSubdate, splitReg.split(s))))
    else:
        return 0
    
class Lightling:
    
    def extractEntities(self, x):  
        return {
            "phone"  : genericExtractor(phone, x),
            "email"  : genericExtractor(email, x),
            "url"    : genericExtractor(url,x),
            "salary" : genericExtractor(salary,x),
            "job"    : genericExtractor(job,x),
            "birthDate"    : genericExtractor(birth,x),
        }
    
    def extractSubdate(self,x):
    
        return match(x,
                period, exPer(x),
                jan, dater(jan,1,x),
                feb, dater(feb,2,x),
                mar, dater(mar,3,x),
                apr, dater(apr,4,x),
                may, dater(may,5,x) ,
                jun, dater(jun, 6,x),
                jul, dater(jul, 7,x),
                aug, dater(aug, 8,x),
                sep, dater(sep, 9,x),
                octb, dater(octb, 10,x),
                nov, dater(nov, 11,x),
                dec, dater(dec, 12,x),
                current, dt.today().date(),            
                digits, lambda t: dt.strptime(digits.search(t)[0], "%m.%Y"),

                _, 0
            )


