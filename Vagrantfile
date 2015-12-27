# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.synced_folder ".", "/opt/code"

  config.vm.provision :shell, :inline => <<-SHELL
     echo 'LC_ALL="en_US.UTF-8"' > /etc/default/locale
  SHELL

  config.vm.provision :ansible do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end

  config.vm.provision :shell, :inline => <<-SHELL
    sudo -i -u postgres createuser dotfile
    sudo -i -u postgres createdb dotfile
    sudo -i -u postgres psql -c "ALTER USER dotfile WITH ENCRYPTED PASSWORD 'password'"
    sudo /opt/venv/bin/python3 /opt/code/run.py create_db
    sudo /opt/venv/bin/python3 /opt/code/run.py db stamp -d /opt/code/migrations head
  SHELL
end
