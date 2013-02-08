import os,sys,ctypes  
      
gpib=getattr(ctypes.windll,"gpib-32")  
      
RQS = (1<<11)  
SRQ = (1<<12)  
TIMO = (1<<14)  
      
class Gpib:  
        def __init__(self,name='gpib0'):  
                self.id = gpib.ibfindA(name)  
	
	def set_term_CR(self):
		gpib.ibeos(self.id, 0x140D)

      
        def close(self):
                gpib.ibonl(self.id,0)  
      
        def write(self,str):  
                gpib.ibwrt(self.id, str,len(str))
                
        def read(self,leng=512):  
                result = ctypes.c_char_p('\000' * leng)  
                retval = gpib.ibrd(self.id,result,leng)  
                return result.value  
      
        def readb(self,leng=512):  
                result = ctypes.c_buffer(leng)  
                retval = gpib.ibrd(self.id,result,leng)  
                return result.raw  
      
        def clear(self):  
                gpib.ibclr(self.id)  
      
        def rsp(self):  
                result = ctypes.c_char_p('\000')  
                self.spb = gpib.ibrsp(self.id,result)  
                if len(result.value)>0:  
                        return ord(result.value)  
                else:  
                        return -256  
