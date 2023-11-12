from Commandline import docker

if __name__ == "__main__":
    dc = docker.DockerCombine()
    dc.addFiles(["docker-minecraft.yml", "docker-nginx.yml"])
    dc.combine(["services", "networks", "volumes"])
    dc.print()
    dc.saveMaster("test.yml")