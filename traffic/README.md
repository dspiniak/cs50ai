STRUCTURE
i. convolution and pooling
    1) 1st layer - learn edges and colors
    2) 2nd layer - learn higher-level features (objects and complex shapes)
ii. flattening
iii. neural network
    1) 3rd layer - hidden layers (need to detect complex shapes)

EXPERIMENTS for test model with 4 categories
1. Changed convolution to 2x2, achieved .94 accuracy
2. Changed convolution to 4x4, achieved .955 accuracy
3. Changed hidden layers to 256, achieved .94
4. Added another hidden layer of 64, achieved .84
5. Changed convolution to 64 filters, achieved .79
5. Changed convolution to 16 filters, achieved .87
Result = change convolution to 4x4

EXPERIMENTS for real model
1. Started with .78 accuracy
2. Changed convolution to 6x6, achieved .83
3. Changed maxpool to (3,3), achieved .70
4. Added new convolution layer with 16 filters, achieved 0.1
Result = change convolution to 6x, maxpool to 3x3

    Conv	MaxPooling	Hidden Layers	Ouput	Accuracy
32, 3x3	2,2	• 128	• dense	.94
        • 0.5 dropout	• softmax
2x2				.36
4x4				.955
        256		.94
        128, step function		
        1. adding another 64 layer 		.84
64		• 128		.79
        • 0.5 dropout
16				.87
32				.78
6x6				.83
    3,3			.70
• new conv layer, 16 filters				0.1
