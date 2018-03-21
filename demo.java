package test;

public class demo {
	 /** 
     * ����pdf2htmlEX��pdf�ļ�ת��Ϊhtml�ļ� 
     * @param command ����exe���ַ��� 
     * @param pdfName ��Ҫת����pdf�ļ����� 
     * @param htmlName ���ɵ�html�ļ����� 
     * @return 
     */  
    public static boolean pdf2html(String command,String pdfName,String htmlName){  
        Runtime rt = Runtime.getRuntime();  
        try {  
            Process p = rt.exec(command);  
            StreamGobbler errorGobbler = new StreamGobbler(p.getErrorStream(), "ERROR");                
              // kick off stderr    
            errorGobbler.start();    
            StreamGobbler outGobbler = new StreamGobbler(p.getInputStream(), "STDOUT");    
              // kick off stdout    
            outGobbler.start();   
            int w = p.waitFor();  
            System.out.println(w);  
            int v = p.exitValue();  
            System.out.println(v);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
        }  
        return false;  
    }  
    
    public static void main(String[] args) {
    	String d="20180108";
    	for(int i=1;i<=9;i++){
    		String temp="rmrb"+d+"0"+i;
    		 pdf2html("E:\\Code\\newspaper\\pdfh5\\pdf2htmlEX.exe E:\\Code\\newspaper\\pdf\\"+temp+".pdf  "+temp+".html",temp+".pdf",temp+".html");  
    	}
    	System.out.println("Complete!!!");      
    }  
}
