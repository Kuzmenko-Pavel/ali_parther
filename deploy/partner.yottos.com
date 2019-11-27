upstream partner_backend_http {
    server 192.168.0.16:8787 weight=100 max_fails=10  fail_timeout=5s;
    server 192.168.0.17:8787 weight=1 max_fails=10  fail_timeout=5s;
    server 192.168.0.18:8787 weight=1 max_fails=10  fail_timeout=5s;
    server 192.168.0.19:8787 weight=1 max_fails=10  fail_timeout=5s;
    keepalive 120;
}

upstream partner_backend_worker {
    server unix:/tmp/ali_parther/ali_partner1.sock;
    server unix:/tmp/ali_parther/ali_partner2.sock;
    server unix:/tmp/ali_parther/ali_partner3.sock;
    server unix:/tmp/ali_parther/ali_partner4.sock;
}


server {
    listen  212.113.34.136:80;
    listen  212.113.34.136:443 ssl http2;
	server_name partner.yottos.com;
	#access_log  /var/log/nginx/partner.yottos.com.access.log;
    error_log /var/log/nginx/partner.yottos.com.error.log;
    root /var/www/ali_parther;
    charset utf-8;
    more_set_headers 'Strict-Transport-Security: max-age=31536000; includeSubDomains';
    more_set_headers 'X-Robots-Tag "noindex, nofollow"';
    http2_push_preload on;

    location / {
    proxy_pass http://partner_backend_http;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_connect_timeout 120s;
    proxy_send_timeout 120s;
    proxy_read_timeout 180s;
    proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
    proxy_next_upstream_tries 5;
    }
}

server {
    listen 8787 reuseport fastopen=500 backlog=1024;
	server_name partner.yottos.com;
	#access_log  /var/log/nginx/dummy.partner_backend_worker.access.log;
    error_log /var/log/nginx/dummy.partner_backend_worker.error.log;
    root /var/www/rg.yottos;
    charset utf-8;
    set $cors "";
    if ($http_origin ~* (.*\.yottos.com)) {
        set $cors "true";
    }
    location / {
        #access_log  /var/log/nginx/partner_backend_worker.access.log;
        error_log /var/log/nginx/partner_backend_worker.error.log;
        proxy_pass http://partner_backend_worker;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_http_version 1.1;
        proxy_redirect off;
        proxy_buffering off;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 1;
    }

    location /static/ {
        expires    10d;
        add_header  Cache-Control  'public';
        alias /var/www/ali_parther/ali_partner/static/;
    }

}
