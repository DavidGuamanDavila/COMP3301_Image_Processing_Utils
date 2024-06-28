%Q1
F_rgb = imread('../imgs/moonlanding.png');

if size(F_rgb, 3) == 3
    F = rgb2gray(F_rgb);
else
    F = F_rgb;
end

figure, imshow(F, []), title('Original Image');
drawnow;

im_size=size(F); % Obtain the size of the image
P=2*im_size(1); % Optaining padding parameters as 2*image size
Q=2*im_size(2); % Optaining padding parameters as 2*image size

FTIm = fft2(double(F), P, Q);

FTIm_shifted = fftshift(FTIm); % Center the spectrum

FSmax = max(FTIm_shifted(:));% Find the maximum value of the frequency spectrum

disp(['Maximum value of the frequency spectrum: ', num2str(FSmax)]);

%Q2
% figure, imshow(FTIm_shifted, []), title('Centered FT Raw of Original');
% drawnow;

FTI = log(1 + abs(FTIm_shifted)); % Calculate the magnitude of the frequency spectrum

figure, imshow(FTI, []), title('Centered FT of Original with Magnitude Enhanced');
drawnow;

% Q3
% Define the parameters
radius = 100; % Distance from the center
angles = [0, 45, 90, 135, 180, 225, 270, 315]; % Angles in degrees for the points

% Calculate coordinates of the points on the circle
center = [P/2 + 1, Q/2 + 1]; % Center of the FFT image
points = zeros(8, 2);
for i = 1:length(angles)
    theta = deg2rad(angles(i));
    x = round(center(1) + radius * cos(theta));
    y = round(center(2) + radius * sin(theta));
    points(i, :) = [x, y];
end

% Set noise at the specified points
FTIm_noisy = FTIm_shifted;
for i = 1:size(points, 1)
    x = points(i, 1);
    y = points(i, 2);
    % Set the 3x3 neighborhood around the point to FSmax/10
    FTIm_noisy(x-1:x+1, y-1:y+1) = FSmax / 10;
end

FTI_noisy = log(1 + abs(FTIm_noisy));
figure, imshow(FTI_noisy, []), title('Centered FT with Noise Introduced');
drawnow;

%Q4
FTIm_noisy = ifftshift(FTIm_noisy); % Shift back to original position
F_noisy = real(ifft2(FTIm_noisy)); % Convert to spatial domain

% Resize the image to undo padding
F_noisy = F_noisy(1:im_size(1), 1:im_size(2));

% Scale the noisy image for display
F_noisy_scaled = mat2gray(F_noisy);

% Display the noisy image
figure, imshow(F_noisy_scaled), title('Noisy Image');
drawnow; 




%Q5