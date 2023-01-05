# Indra
Indra ([Indra otsutuki](https://naruto.fandom.com/wiki/Indra_%C5%8Ctsutsuki)) is an authentication method based of [hand seals](https://naruto.fandom.com/wiki/Hand_Seal) from anime Naruto. 
Sorry to dissapoint you but fire won't come out of your mouth and lightning wont appeared in your hand after performing the hand signs :').
Currently only supported on GNU + Linux based os and only tested on [Pop-OS 22.04](https://pop.system76.com/)

## Disclaimer
This authentication method is for fun only and to help you to stay true to your ninja way.
Please be aware when you want to install and use it.

## Installation Guide
* In order to enable this authentication on your machine you need to clone this repository and install some python library and dependency
    ```
    git clone https://github.com/SiahaanBernard/indra
    cd indra
    ```
* Install required python libraries
    ```
    sudo pip install -f src/requirements.txt
    ```

* Install the required linux libraries
    ```
    sudo apt install nvidia-cuda-toolkit
    sudo apt install nvidia-cudnn
    sudo apt install python-pam
    ```

* Copy all files under src directory to /lib/security/indra
    ```
    sudo cp src /lib/security/indra -r
    sudo chmod 755 -R /lib/security/indra
    ```

* Copy the pam configuration file to /usr/share/pam-configs/ and update the pam configuration
    ```
    sudo cp src/pam-config/indra  /usr/share/pam-configs
    sudo pam-auth-update --package
    ```
* symlink the cli to /usr/bin/local to use cli to configure indra
    ```
    sudo ln -s /lib.security/indra/cli.py /usr/local/bin/indra
    ```

## Configure Password
* Run the following command, and insert the chain hand sign as your password
    ```
    sudo indra configure
    ```

## Demo
1. TODO

## Credits
Special thanks to [boltgolt](https://github.com/boltgolt) and [Kazuhito00](https://github.com/Kazuhito00) for open sourcing their project and become inspiration for this project. Go checkout their project:
- [Howdy](https://github.com/boltgolt/howdy)
- [Naruto Handsign Detection](https://github.com/Kazuhito00/NARUTO-HandSignDetection)

## Contributing
Contributions are welcome if you want to help improve this project.For now there is no guidance for contributing, if you are willing, please create an issue and pull request on this github.
