s1=float(input('Enter the first side of the triangle: '))
s2=float(input('Enter the second side of the triangle: '))
s3=float(input('Enter the third side of the triangle: '))

#Calculate the semi-perimeter
sp=(s1+s2+s3)/2

#Calculate the area
area=(sp*(sp-s1)*(sp-s2)*(sp-s3))**0.5

print('The area of the triangle is %0.4f'%area)