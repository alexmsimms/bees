// ******************************************************************//
// A class to handle general neural networks in matrix form.         //
// ------------------------------------------------------------------//
// The code was specifically designed to be called from neat-python  //
// and was partially based on the source code provided by Randall    //
// D. Beer at mypage.iu.edu/~rdbeer/                                 //
// ******************************************************************//

#ifndef _ANN_H_
#define _ANN_H_

#include <Python.h>
#include <math.h>
#include "VectorMatrix.h"

//using namespace std;

class ANN {
    public:
        // The constructor
        ANN(int how_many_inputs = 0, int newsize = 0);
        // The destructor
        //~ANN();

        void SetConnectionWeight(int from, int to, double value) {
            weights[from][to] = value;
            };

        void set_sensory_weight(int from, int to, double value) {sensory_weights[from][to] = value;};

        void setNeuronParameters(int i, double bias, double gain, int type) {
            biases[i] = bias;
            response[i] = gain;
            neuron_type[i] = type;
        };
        
        double get_neuron_response(int i) { return response[i]; }
        double get_neuron_bias(int i) { return biases[i]; }

        void setNeuronOutput(int i, double output) {
            outputs[i] = output;
        };

        double NeuronOutput(int i) { return outputs[i]; };

        // serial activation method (for feedforward topologies)
        PyObject* sactivate(PyObject* inputs); 
        // parallel activation method (for recurrent neural networks)
        PyObject* pactivate(PyObject* inputs);

        // flushes all neuron's output
        void flush();

        void set_logistic(bool option) {
            logistic = option;
        };
              
        double sigmoid(double x, double response);

       // void use_fast_sigmoid(bool b) {
       //     fast_sigmoid = b;
       // }

   private:        
        int size;      // number of neurons (hidden + output)
        int sensors;   // number of sensors (inputs)
        bool logistic; // activation type (exp or tanh)
        
        // neuron's properties
        TVector<double> states, outputs, biases, response;
        
        // each neuron has a type: 0 (hidden) or 1 (output)
        TVector<int> neuron_type;
        
        // each network is composed of two matrices:
        // one to specify how the inputs are connected
        // to neurons and other to specify inter-neuron
        // connections (hidden and outputs)
        TMatrix<double> weights, sensory_weights;


};
#endif
