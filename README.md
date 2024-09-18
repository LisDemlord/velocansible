# Velocansible

Velocansible — это проект, предназначенный для автоматизации развертывания и настройки Velociraptor на серверах и клиентских машинах с использованием Ansible.

## Структура проекта
velocansible/
├── main-host.yml                # Playbook для развертывания Velociraptor на хостах
├── main-clients.yml             # Playbook для развертывания Velociraptor на клиентских машинах
├── inventory/                    # Директория с файлами инвентаризации
│   └── hosts.yml                # Файл инвентаризации, содержащий информацию о хостах
├── roles/                        # Директория с ролями Ansible
│   ├── configuring_firewall/     # Роль для настройки брандмауэра
│   │   └── tasks/                # Директория с задачами роли
│   │       └── main.yml          # Основной файл задач для настройки брандмауэра
│   ├── install_velociraptor_host/ # Роль для установки Velociraptor на хостах
│   │   └── tasks/                # Директория с задачами роли
│   │       └── main.yml          # Основной файл задач для установки Velociraptor на хостах
│   └── install_velociraptor_clients/ # Роль для установки Velociraptor на клиентских машинах
│       └── tasks/                # Директория с задачами роли
│           └── main.yml          # Основной файл задач для установки Velociraptor на клиентских машинах
├── vault.yml                    # Файл с зашифрованными переменными
└── README.md                    # Этот файл

## Установка

1. Убедитесь, что у вас установлен Ansible. Вы можете установить его с помощью pip:

   ```bash
   pip install ansible
   ```

2. Настройте SSH-доступ к вашим серверам и клиентским машинам.

3. Создайте и настройте файл `vault.yml` для хранения зашифрованных переменных.

## Использование

### Развертывание на хостах

Чтобы развернуть Velociraptor на хостах, выполните следующую команду:

```bash
ansible-playbook -i inventory/hosts.yml main-host.yml --vault-password-file=[ваш файл с паролем]
```

### Развертывание на клиентских машинах

Чтобы развернуть Velociraptor на клиентских машинах, выполните следующую команду:

```bash
ansible-playbook -i inventory/hosts.yml main-clients.yml --vault-password-file=[ваш файл с паролем]
```

## Структура ролей

- **configuring_firewall**: Роль для настройки iptables на серверах.
- **install_velociraptor_host**: Роль для установки Velociraptor на серверной части.
- **install_velociraptor_clients**: Роль для установки Velociraptor на клиентских машинах.