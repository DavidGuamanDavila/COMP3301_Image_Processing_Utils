%Q1
F_rgb = imread('../imgs/moonlanding.png');

if size(F_rgb, 3) == 3
    F = rgb2gray(F_rgb);
else
    F = F_rgb;
end

% figure, imshow(F, []), title('Original Image');
% drawnow;

im_size=size(F); % Obtain the size of the image
P=2*im_size(1); % Optaining padding parameters as 2*image size
Q=2*im_size(2); % Optaining padding parameters as 2*image size

FTIm = fft2(double(F), P, Q);

FTIm_shifted = fftshift(FTIm);

FSmax = max(FTIm_shifted(:));

disp(['Maximum value of the frequency spectrum: ', num2str(FSmax)]);

%Q2
% figure, imshow(FTIm_shifted, []), title('Centered FT Raw of Original');
% drawnow;

FTI = log(1 + abs(FTIm_shifted));

% figure, imshow(FTI, []), title('Centered FT of Original with Magnitude Enhanced');
% drawnow;

% Q3
radius = 100; 
angles = [0, 45, 90, 135, 180, 225, 270, 315];

center = [P/2 + 1, Q/2 + 1];
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
% figure, imshow(FTI_noisy, []), title('Centered FT with Noise Introduced');
% drawnow;

%Q4
FTIm_noisy = ifftshift(FTIm_noisy); 
F_noisy = real(ifft2(FTIm_noisy));

F_noisy = F_noisy(1:im_size(1), 1:im_size(2));

F_noisy_scaled = mat2gray(F_noisy);

% figure, imshow(F_noisy_scaled), title('Noisy Image');
% drawnow; 


%Q5
FTIm_noisy = fft2(double(F_noisy), P, Q);

FTIm_noisy_shifted = fftshift(FTIm_noisy);

FTI_noisy_centered = log(1 + abs(FTIm_noisy_shifted));
figure, imshow(FTI_noisy_centered, []), title('Centered FT of Noisy Image');
drawnow;

% %Q6
% D0 = 100;
% W = 8;
% n = 4; % Butterworth order
% 
% %https://www.mathworks.com/help/matlab/ref/meshgrid.html
% [U, V] = meshgrid(1:im_size(2), 1:im_size(1));
% D = sqrt((U - im_size(2) / 2).^2 + (V - im_size(1) / 2).^2);
% 
% H_ideal = ones(im_size(1), im_size(2));
% H_ideal(D >= (D0 - W / 2) & D <= (D0 + W / 2)) = 0;
% 
% H_butterworth = 1 ./ (1 + ((D .* W) ./ (D.^2 - D0^2)).^(2 * n));
% 
% H_gaussian = 1 - exp(-((D.^2 - D0^2) ./ (D .* W)).^2);
% 
% figure, imshow(H_ideal, []), title('Ideal Band-Reject Filter');
% drawnow;
% 
% figure, imshow(H_butterworth, []), title('Butterworth Band-Reject Filter with order n = 4');
% drawnow;
% 
% figure, imshow(H_gaussian, []), title('Gaussian Band-Reject Filter');
% drawnow;
