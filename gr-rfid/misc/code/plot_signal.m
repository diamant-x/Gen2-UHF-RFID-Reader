clc
clear all
close all

fi_1 = fopen('../data/source','rb'); 
%2021-01-22_float32-source_Example-RN16
x_inter_1 = fread(fi_1, 'float32');
fclose(fi_1);

fi_2 = fopen('../data/matched_filter','rb'); 
x_inter_2 = fread(fi_2, 'float32');
fclose(fi_2);
 
fi_3 = fopen('../data/gate','rb'); 
x_inter_3 = fread(fi_3, 'float32');
fclose(fi_3);

fi_4 = fopen('../data/decoder_complex','rb'); 
x_inter_4 = fread(fi_4, 'float32');
fclose(fi_4);

fi_5 = fopen('../data/decoder_float','rb'); 
x_inter_5 = fread(fi_5, 'float32');
fclose(fi_5);

% if data is complex
x_1 = abs(x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end));
x_2 = abs(x_inter_2(1:2:end) + 1i*x_inter_2(2:2:end));
x_3 = abs(x_inter_3(1:2:end) + 1i*x_inter_3(2:2:end));
x_4 = abs(x_inter_4(1:2:end) + 1i*x_inter_4(2:2:end));
x_5 = x_inter_5; % Float already.

figure('Name','UHF RFID Output Stages', 'WindowState', 'maximized');
subplot(2,3,1)
plot(abs(x_1))
title('Source')

subplot(2,3,2)
plot(abs(x_2))
title('FIR Filter')

subplot(2,3,3)
plot(abs(x_3))
title('Gate Block')

subplot(2,3,4)
plot(abs(x_4))
title('Decoder Block (| RN16 | EPC |)')

subplot(2,3,5)
plot(abs(x_5))
ylim([-0.1, 1.1]);
title('RN16 bits')
