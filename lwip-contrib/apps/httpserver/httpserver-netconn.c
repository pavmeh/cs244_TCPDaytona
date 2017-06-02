
#include "lwip/opt.h"
#include "lwip/arch.h"
#include "lwip/api.h"
#include <stdio.h>
#include <stdlib.h>
#include "httpserver-netconn.h"

#if LWIP_NETCONN

#ifndef HTTPD_DEBUG
#define HTTPD_DEBUG         LWIP_DBG_OFF
#endif

const static char http_html_hdr[] = "HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n";
//const static char http_index_html[] = "<html><head><title>Congrats!</title></head><body><h1>Welcome to our lwIP HTTP server!</h1><p>This is a small test page, served by httpserver-netconn.</body></html>";

static char *http_index_html;
static size_t index_len;
/** Serve one HTTP connection accepted in the http thread */
static void
http_server_netconn_serve(struct netconn *conn)
{
  struct netbuf *inbuf;
  char *buf;
  u16_t buflen;
  err_t err;
  
  /* Read the data from the port, blocking if nothing yet there. 
   We assume the request (the part we care about) is in one netbuf */
  err = netconn_recv(conn, &inbuf);
  
  if (err == ERR_OK) {
    netbuf_data(inbuf, (void**)&buf, &buflen);
    
    /* Is this an HTTP GET command? (only check the first 5 chars, since
    there are other formats for GET, and we're keeping it very simple )*/
    if (buflen>=5 &&
        buf[0]=='G' &&
        buf[1]=='E' &&
        buf[2]=='T' &&
        buf[3]==' ' &&
        buf[4]=='/' ) {
      
      /* Send the HTML header 
             * subtract 1 from the size, since we dont send the \0 in the string
             * NETCONN_NOCOPY: our data is const static, so no need to copy it
       */
      netconn_write(conn, http_html_hdr, sizeof(http_html_hdr)-1, NETCONN_NOCOPY);
      
      /* Send our HTML page */
      netconn_write(conn, http_index_html, index_len-1, NETCONN_NOCOPY);
    }
  }
  /* Close the connection (server closes in HTTP) */
  netconn_close(conn);
  
  /* Delete the buffer (netconn_recv gives us ownership,
   so we have to make sure to deallocate the buffer) */
  netbuf_delete(inbuf);
}

static void
http_server_read_index() {
  FILE *fp = fopen("index.html", "r");
  if (fp != NULL) {
      /* Go to the end of the file. */
      if (fseek(fp, 0L, SEEK_END) == 0) {
          /* Get the size of the file. */
          long temp = ftell(fp);
          if (temp == -1) { printf("Could nto read file\n"); exit(1);}
          index_len = (size_t) temp;
          /* Allocate our buffer to that size. */
          http_index_html = malloc(sizeof(char) * (index_len + 1));

          /* Go back to the start of the file. */
          if (fseek(fp, 0L, SEEK_SET) != 0) { /* Error */ }

          /* Read the entire file into memory. */
          size_t newLen = fread(http_index_html, sizeof(char), index_len, fp);
          if ( ferror( fp ) != 0 ) {
              fputs("Error reading file", stderr);
              free(http_index_html);
          } else {
              http_index_html[newLen++] = '\0'; /* Just to be safe. */
          }
      }
      fclose(fp);
  }
  else {
    printf("index.html does not exist.\n");
    exit(1);
  }
}

/** The main function, never returns! */
static void
http_server_netconn_thread(void *arg)
{
  struct netconn *conn, *newconn;
  err_t err;
  LWIP_UNUSED_ARG(arg);
  http_server_read_index();
  /* Create a new TCP connection handle */
  conn = netconn_new(NETCONN_TCP);
  LWIP_ERROR("http_server: invalid conn", (conn != NULL), return;);
  
  /* Bind to port 80 (HTTP) with default IP address */
  netconn_bind(conn, NULL, 80);
  
  /* Put the connection into LISTEN state */
  netconn_listen(conn);
  
  do {
    err = netconn_accept(conn, &newconn);
    if (err == ERR_OK) {
      http_server_netconn_serve(newconn);
      netconn_delete(newconn);
    }
  } while(err == ERR_OK);
  LWIP_DEBUGF(HTTPD_DEBUG,
    ("http_server_netconn_thread: netconn_accept received error %d, shutting down",
    err));
  free(http_index_html);
  netconn_close(conn);
  netconn_delete(conn);
}

/** Initialize the HTTP server (start its thread) */
void
http_server_netconn_init()
{
  sys_thread_new("http_server_netconn", http_server_netconn_thread, NULL, DEFAULT_THREAD_STACKSIZE, DEFAULT_THREAD_PRIO);
}

#endif /* LWIP_NETCONN*/
