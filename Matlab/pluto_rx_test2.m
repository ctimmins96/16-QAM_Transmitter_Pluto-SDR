%% MATLAB simulation for 16-QAM system
close all;

% Define some initial variables
N = 10;
fs = 30720000;
fc = fs/N;

start_bits = ['0','7','B','F'];
end_bits = ['1','6','E','A'];
mess_bits = ['1','0','C','4','9','B','2','E'];

sb = bits2sin(start_bits,fc,fs);
eb = bits2sin(end_bits,fc,fs);

tx_bits = [start_bits,'1','0','C','4','9','B','2','E',end_bits];
tx = bits2sin(tx_bits,fc,fs);

% Find start bits and end bits in received data

% n = 1:length(rxdata(1,:));
% s_idx = 1;
%
% sb_p = padding(sb,0,length(rxdata));
%
% [xc_sb, lags] = xcorr(rxdata,sb_p);
% plot(lags,xc_sb);
% title('Cross correlation: Start Bits');
%
% [~, s_idx] = max(xc_sb);
%
% s_idx = lags(s_idx);
%
% figure;
% plot(rxdata(s_idx:(s_idx + length(sb) - 1)),'*-');
% hold on;
% plot(sb,'*-');
% legend('Received Data','Start Bits');
% title('Possible Start Bits');

header = [sb, zeros([1,length(mess_bits)*N]), eb];
header_p = padding(header,0,length(rxdata));

[xc_h,lags] = xcorr(rxdata,header_p);
plot(lags,xc_h);
title('Header Cross Correlation');

[~, temp] = max(xc_h);
s_idx = lags(temp) + 1;

n = s_idx:(s_idx + length(header) - 1);

figure;
plot(n,rxdata(n),n,header);
legend('Received Data','Header');
title('Possible Header');
e_idx2 = n(end);

% Create new, condensed variable for received data
rxdata1 = rxdata(s_idx:e_idx2);

% Create found_bits variable to store results in
found_bits = [''];

% Loop through tx variable, partition bits, decode partitions
for k = 1:length(rxdata1)/N
    part = rxdata(N*(k - 1) + 1 : N*k);

    % TODO: Possibly FIR Filter partitions

    f_amp = max(part);
    f_pha = 0;
    max_cor = 0;
    % TODO: Change structure of nearest neighbor approximation in
    % incorporate a custom delay
    for l = 1:N
        a = 1:N;
        tst_wav = sin(2*pi*(fc/fs)*(a + (l-1)));
        tmp = norm_xcor(part,tst_wav);
        if (tmp > max_cor)
            max_cor = tmp;
            f_pha = 2*pi*(l-1)/N;
        end
    end

    found_sin = f_amp*cos(f_pha) + 1j*f_amp*sin(f_pha);
    found_bits(k) = near_neighbor(found_sin);
end

% Display found_bits variable
disp(['Found Bits:']);
disp(found_bits);
disp(['Transmitted Bits:']);
disp(tx_bits);
%% Function definitions

bits2sine
function tx = bits2sin(tx_bits,fc,fs)

    N = round(fs/fc);
    tx = zeros([1, N*length(tx_bits)]);

    for ii = 1:length(tx_bits)

        z = KEY_16QAM(tx_bits(ii));

        for k = 1:N
            tx(k + N*(ii - 1)) = real(z) * sin(2*pi*fc*k/fs) + 1j*imag(z)*cos(2*pi*fc*k/fs);
        end

    end

end

% KEY_16QAM
function z = KEY_16QAM(key)

z = 0;

switch(key)
case '0'
    z = 1 + 1j;
case '1'
    z = 1 - 1j;
case '2'
    z = -1 - 1j;
case '3'
    z = -1 + 1j;
case '4'
    z = 1 + 2j;
case '5'
    z = 2 + 2j;
case '6'
    z = 2 + 1j;
case '7'
    z = 2 - 1j;
case '8'
    z = 2 - 2j;
case '9'
    z = 1 - 2j;
case 'A'
    z = -1 - 2j;
case 'B'
    z = -2 - 2j;
case 'C'
    z = -2 - 1j;
case 'D'
    z = -2 + 1j;
case 'E'
    z = -2 + 2j;
case 'F'
    z = -1 + 2j;
end

end

% norm_xcor
function xcor_val = norm_xcor(x1,x2)

e1 = x1*(x1');
e2 = x2*(x2');

xcor_val = 0;

% Pad x1 and x2 with zeros
x2_p = [zeros([1 (length(x1) - 1)]), x2, zeros([1 (length(x1) - 1)])];

for k = 1:(length(x1) - 1 + length(x2))
    tmp = x2_p(k:(k + length(x1) - 1));
    xsum = sum(tmp.*x1)/sqrt(e1*e2);
    if (xsum > xcor_val)
        xcor_val = xsum;
    end
end


end

% near_neighbor
function bit = near_neighbor(x)

bit = '0';
bits = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'];

dist = 100;
for k = 1:length(bits)
    if (abs(x - KEY_16QAM(bits(k))) <= dist)
        dist = abs(x - KEY_16QAM(bits(k)));
        bit = bits(k);
    end
end

end

% Padding Function
function padded = padding(part,n,L)

padded = zeros([1 L]);

padded(n+1:n + length(part)) = part;

end
