Automate File Upload securely to AWS S3 - Supporting encryption on flight and at rest

*Cloud Services used*
-	S3
-	ACM
-	Route53
-	ALB


automate background run :  *ohup python3 server.py > server.log 2>&1 &*

Check if background process is up : *ps aux | grep server.py*


Step I
Configuring Domain on Route 53 with ALB for SSL Termination
Domain Setup in Route 53


Created a hosted zone for inspirenetwork.net.


Added an A record (data.inspirenetwork.net) as an alias pointing to the Application Load Balancer (ALB).


Application Load Balancer (ALB) Configuration


Created an ALB with listeners:


Port 443 (HTTPS) with SSL certificate from AWS ACM


(Optionally) Port 80 forwarding to 443 for redirection


Registered EC2 instance (running Apache + Flask) as a target.


SSL Termination


SSL handled at ALB (terminates HTTPS).


ALB forwards traffic to Apache over HTTP (port 80) internally.


Domain Resolution


https://data.inspirenetwork.net now securely routes traffic via:


Route 53 → ALB (SSL termination) → Apache reverse proxy → Flask app



Step II

Summary: Flask + Apache + HTTPS Integration
Flask App
 Built a Flask API running on localhost:5000 with an endpoint /generate-upload-url.


Apache Reverse Proxy
 Configured Apache2 on EC2 to act as a reverse proxy, forwarding requests from:
 https://data.inspirenetwork.net/generate-upload-url to to the Flask app on 127.0.0.1:5000.
Modules Enabled
 Enabled Apache modules: sudo a2enmod proxy proxy_http headers
Apache Config (port 80)
Added to /etc/apache2/sites-available/000-default.conf:
ProxyPreserveHost On
ProxyPass /generate-upload-url http://127.0.0.1:5000/generate-upload-url
ProxyPassReverse /generate-upload-url http://127.0.0.1:5000/generate-upload-url
HTTPS via ALB
SSL termination handled at AWS ALB; Apache receives HTTP traffic on port 80.
Frontend JS
Updated JavaScript to send POST requests to the public HTTPS endpoint and parse the JSON response.










-	
