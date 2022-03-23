#version 330 core

in vec3 OutColor;
in vec3 OutNormal;

out vec4 FragColor;

void main()
{
  vec3 LightDirection = normalize(vec3(0.0, 0.0, 1.0));
  float LightIntensity = 1.0;

  vec3 OutNormal = normalize(OutNormal);
  float Lambertian = max(0, dot(LightDirection, OutNormal));
  FragColor = vec4(OutColor*0.5 + OutColor * LightIntensity * Lambertian, 1.0);
}