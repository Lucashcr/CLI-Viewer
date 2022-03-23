#version 330 core

uniform mat4 ModelViewProjection;
uniform mat4 NormalMatrix;

layout (location = 0) in vec3 InPosition;
layout (location = 1) in vec3 InColor;
layout (location = 2) in vec3 InNormal;

out vec3 OutColor;
out vec3 OutNormal;

void main()
{
  OutNormal = vec3(NormalMatrix * vec4(InNormal, 0.0));
  OutColor = InColor;
  gl_Position = ModelViewProjection * vec4(InPosition, 1.0);
}