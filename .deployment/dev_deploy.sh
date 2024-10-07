ssh -o StrictHostKeyChecking=no -tt digipass@dev.digipass.dolphinchat.ai  <<"EOF"
    cd /home/digipass/epass-appointment
    git stash
    git checkout dev
    git fetch origin dev
    git reset --hard origin/dev
    git pull origin dev
    # Build - Bring Down - Bring Up
    sudo systemctl restart epass-appointment.service
    exit
EOF
