sudo apt update && sudo apt upgrade
sudo usermod -aG sudo [username]
sudo apt install net-tools
ifconfig (verify server has an ip address)
sudo apt install openssh-server
sudo systemctl enable –now ssh
sudo systemctl status ssh (verify ssh is working)
sudo apt install apache2
sudo ufw app list (verify apache2 is listed)
sudo apt install mariadb-server
sudo mysql_secure_installation
n
You can change the password if you want
y
y
y
y
sudo systemctl status mariadb (verify mariadb is working)
sudo apt install php libapache2-mod-php php-mysql
sudo apt-get install php-mysqli
php -v (verify php is on the latest version)
sudo chown -R www-data:www-data /var/www
sudo chmod -R 777 /var/www
sudo service apache2 restart (type in the server’s ip address into a browser and verify that apache is working)
sudo nano /var/www/html/phpinfo.php
Type the following:
<?php 
  phpinfo();
?>
Save and exit.
Type serverip/phpinfo.php into a searchbar and verify php is working
