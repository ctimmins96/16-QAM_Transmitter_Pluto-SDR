%% MATLAB simulation for 16-QAM system
close all;

% Define some initial variables
N = 24;
fs = 1e9;
fc = fs/N;
tx_bits = ['0','1','7','F','9','4','B','D','3'];

% Generate and Plot Transmit Data (also generate noise)
tx = bits2sin(tx_bits,fc,fs);
tx_s = tx;

varnc = 0.4;
tx_noise = (varnc)*randn([1, length(tx)]);
tx = tx_s + tx_noise;

n = (1:length(tx))/fs;

plot(n,tx_s,n,tx);
xlabel('Sample');
ylabel('Voltage');
legend('Transmitted','Received');

% Create found_bits variable to store results in
found_bits = [''];

% Loop through tx variable, partition bits, decode partitions
for k = 1:length(tx)/N
    part = tx(N*(k - 1) + 1 : N*k);

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

% bits2sine
function tx = bits2sin(tx_bits,fc,fs)

    N = round(fs/fc);
    tx = zeros([1, N*length(tx_bits)]);

    for ii = 1:length(tx_bits)

        z = KEY_16QAM(tx_bits(ii));

        amp = abs(z);
        pha = angle(z);

        for k = 1:N
            tx(k + N*(ii - 1)) = amp * sin(2*pi*fc*k/fs + pha);
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
