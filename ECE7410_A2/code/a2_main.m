%Q1
F_rgb = imread('../imgs/moonlanding.png');

if size(F_rgb, 3) == 3
    F = rgb2gray(F_rgb);
else
    F = F_rgb;
end

figure(1), imshow(F, []), title('Q1: Original Image');
drawnow;

im_size=size(F); % Obtain the size of the image

FTIm = fft2(double(F));

FTIm_shifted = fftshift(FTIm);

FSmax = max(FTIm_shifted(:));

disp(['Maximum value of the frequency spectrum: ', num2str(FSmax)]);

%Q2
figure(2), imshow(FTIm_shifted, []), title('Q2: Centered FT Raw of Original');
drawnow;

FTI = log(1 + abs(FTIm_shifted));

figure(3), imshow(FTI, []), title('Q2: Centered FT of Original with Magnitude Enhanced');
drawnow;

%Q3
radius = 100; 
angles = [0, 45, 90, 135, 180, 225, 270, 315];

center = [im_size(1)/2 + 1, im_size(2)/2 + 1];
points = zeros(8, 2);

for i = 1:length(angles)
    theta = deg2rad(angles(i));
    x = round(center(1) + radius * cos(theta));
    y = round(center(2) + radius * sin(theta));
    points(i, :) = [x, y];
end


FTIm_noisy = FTIm_shifted;
for i = 1:size(points, 1)
    x = points(i, 1);
    y = points(i, 2);
    FTIm_noisy(x-1:x+1, y-1:y+1) = FSmax / 10;
end

FTI_noisy = log(1 + abs(FTIm_noisy));
figure(4), imshow(FTI_noisy, []), title('Q3: Centered FT with Manual Noise Introduced');
drawnow;

%Q4
FTIm_noisy = ifftshift(FTIm_noisy); 
F_noisy = real(ifft2(FTIm_noisy));

F_noisy = F_noisy(1:im_size(1), 1:im_size(2));

F_noisy_scaled = mat2gray(F_noisy);

figure(5), imshow(F_noisy_scaled), title('Q4: Noisy Image Spatial Domain');
drawnow; 


%Q5
FTIm_noisy = fft2(double(F_noisy));
FTIm_noisy_shifted = fftshift(FTIm_noisy);
FTI_noisy_centered = log(1 + abs(FTIm_noisy_shifted));

figure(6), imshow(FTI_noisy_centered, []), title('Q5: Centered FT of Noisy Image');
drawnow; 
 
%Q6
D0 = 100;
W = 8;
n = 4; % Butterworth order

%https://www.mathworks.com/help/matlab/ref/meshgrid.html
[U, V] = meshgrid(1:im_size(2), 1:im_size(1));
D = sqrt((U - im_size(2) / 2).^2 + (V - im_size(1) / 2).^2);

H_ideal = ones(im_size(1), im_size(2));
H_ideal(D >= (D0 - W / 2) & D <= (D0 + W / 2)) = 0;

H_butterworth = 1 ./ (1 + ((D .* W) ./ (D.^2 - D0^2)).^(2 * n));

H_gaussian = 1 - exp(-((D.^2 - D0^2) ./ (D .* W)).^2);

figure(7), imshow(H_ideal, []), title('Q6:Ideal Band-Reject Filter');
drawnow;

figure(8), imshow(H_butterworth, []), title('Q6:Butterworth Band-Reject Filter with order n = 4');
drawnow;

figure(9), imshow(H_gaussian, []), title('Q6:xGaussian Band-Reject Filter');
drawnow;

% Q7
FTIm_ideal_filtered = FTIm_noisy_shifted .* H_ideal;
FTI_ideal_filtered = log(1 + abs(FTIm_ideal_filtered));
figure(10), imshow(FTI_ideal_filtered, []), title('Q7:FT with Ideal Band-Reject Filter');
drawnow;

FTIm_butterworth_filtered = FTIm_noisy_shifted .* H_butterworth;
FTI_butterworth_filtered = log(1 + abs(FTIm_butterworth_filtered));
figure(11), imshow(FTI_butterworth_filtered, []), title('Q7:FT with Butterworth Band-Reject Filter');
drawnow;

FTIm_gaussian_filtered = FTIm_noisy_shifted .* H_gaussian;
FTI_gaussian_filtered = log(1 + abs(FTIm_gaussian_filtered));
figure(12), imshow(FTI_gaussian_filtered, []), title('Q7:FT with Gaussian Band-Reject Filter');
drawnow;

%Q8
FTIm_ideal_filtered_spatial = ifftshift(FTIm_ideal_filtered);
F_ideal_filtered = real(ifft2(FTIm_ideal_filtered_spatial));
F_ideal_filtered = F_ideal_filtered(1:im_size(1), 1:im_size(2));
F_ideal_filtered_scaled = mat2gray(F_ideal_filtered);
figure(13), imshow(F_ideal_filtered_scaled), title('Q8: Spatial Domain: Ideal Filter');
drawnow;

FTIm_butterworth_filtered_spatial = ifftshift(FTIm_butterworth_filtered);
F_butterworth_filtered = real(ifft2(FTIm_butterworth_filtered_spatial));
F_butterworth_filtered = F_butterworth_filtered(1:im_size(1), 1:im_size(2));
F_butterworth_filtered_scaled = mat2gray(F_butterworth_filtered);
figure(14), imshow(F_butterworth_filtered_scaled), title('Q8: Spatial Domain: Butterworth Filter');
drawnow;

FTIm_gaussian_filtered_spatial = ifftshift(FTIm_gaussian_filtered);
F_gaussian_filtered = real(ifft2(FTIm_gaussian_filtered_spatial));
F_gaussian_filtered = F_gaussian_filtered(1:im_size(1), 1:im_size(2));
F_gaussian_filtered_scaled = mat2gray(F_gaussian_filtered);
figure(15), imshow(F_gaussian_filtered_scaled), title('Q8: Spatial Domain: Gaussian Filter');
drawnow;