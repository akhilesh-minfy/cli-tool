resource "aws_security_group" "my_security_group" {
  name= "cli-tool-sg"
  
  ingress {
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    from_port        = 9090
    to_port          = 9090
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    }
    ingress {
    from_port        = 3000
    to_port          = 3000 
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    }
     ingress {
    from_port        = 9100
    to_port          = 9100
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    }
     ingress {
    from_port        = 9115
    to_port          = 9115
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}



resource "aws_instance" "my_instance" {
  ami           = "ami-0f918f7e67a3323f0"
  instance_type = "t2.micro"
  key_name      = "Day-one-Akhilesh-kp"
  vpc_security_group_ids = [aws_security_group.my_security_group.id]
  tags = {
    Name ="my-instance"
  
}
}