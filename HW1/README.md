用 AWS App Runner 部署一個Flask或tomcat(二選一)的web，顯示 HelloWorld!

素材
python檔, requirement.txt, docker, AWS: ECR, App Runner

流程:  
1.打好python檔, 寫好Flask指令可以呼叫”hello world!”  
2. 創建一个 Dockerfile 来容器化 Flask 應用, 以及創建requirements.txt, 裡面打Flask  
3. 打開powershell, 建構和推送Docker 镜像到AWS  
4. 用AWS創建一個ECR倉庫  
5. 用AWS開App Runner部屬成功!  


