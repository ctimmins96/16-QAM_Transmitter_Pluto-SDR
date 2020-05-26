%% MATLAB simulation for 16-QAM system

% Define some initial variables
fs = 1e9;
fc = fs/100;
N = 100;
tx_bits = ['0','1','7','F'];

% Generate and Plot Transmit Data (also generate noise)
tx = bits2sin(tx_bits,fc,fs);
tx_s = tx;

varnc = 0.4;
tx_noise = (varnc)*randn([1, length(tx)]);
tx = tx_s + tx_noise;

n = (1:length(tx))/fs;

plot(n,tx_s,'*',n,tx,'*');
xlabel('Sample');
ylabel('Voltage');
legend('Transmitted','Received');

% Create initial waveform variables (delete definitions later)
n = 1:N;
p_pi6 = sin(2*pi*fc*n/fs + pi/6);
p_pi4 = sin(2*pi*fc*n/fs + pi/4);
p_pi3 = sin(2*pi*fc*n/fs + pi/3);
p_5pi6 = sin(2*pi*fc*n/fs + 5*pi/6);
p_3pi4 = sin(2*pi*fc*n/fs + 3*pi/4);
p_2pi3 = sin(2*pi*fc*n/fs + 2*pi/3);
p_npi6 = sin(2*pi*fc*n/fs - pi/6);
p_npi4 = sin(2*pi*fc*n/fs - pi/4);
p_npi3 = sin(2*pi*fc*n/fs - pi/3);
p_n5pi6 = sin(2*pi*fc*n/fs - 5*pi/6);
p_n3pi4 = sin(2*pi*fc*n/fs - 3*pi/4);
p_n2pi3 = sin(2*pi*fc*n/fs - 2*pi/3);

phases = [p_pi6; p_pi4; p_pi3; p_5pi6; p_3pi4; p_2pi3; p_npi6; p_npi4; p_npi3; p_n5pi6; p_n3pi4; p_n2pi3; ];

% Create found_bits variable to store results in
found_bits = ['','','',''];

% Loop through tx variable, partition bits, decode partitions
for k = 1:length(tx)/N
    part = tx(N*(k - 1) + 1 : N*k);

    f_amp = max(part);
    f_pha = 0;
    max_cor = 0;
    for l = 1:length(phases(:,1))
        tmp = norm_xcor(part,phases(l,:));
        if (tmp > max_cor)
            max_cor = tmp;
            f_pha = phase_LUT(l);
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

% phase_LUT
function pha = phase_LUT(x)

pha = 0;

switch(x)
    case 1
        pha = pi/6;
    case 2
        pha = pi/4;
    case 3
        pha = pi/3;
    case 4
        pha = 5*pi/6;
    case 5
        pha = 3*pi/4;
    case 6
        pha = 2*pi/3;
    case 7
        pha = -pi/6;
    case 8
        pha = -pi/4;
    case 9
        pha = -pi/3;
    case 10
        pha = -5*pi/6;
    case 11
        pha = -3*pi/4;
    case 12
        pha = -2*pi/3;

end

end

% near_neighbor
function bit = near_neighbor(x)

bit = '0';
bits = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'];

dist = 100;
for k = 1:length(bits)
    if (abs(x - KEY_16QAM(bits(k))) < dist)
        dist = abs(x - KEY_16QAM(bits(k)));
        bit = bits(k);
    end
end

end
