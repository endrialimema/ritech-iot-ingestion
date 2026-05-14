#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <unordered_map>
#include <vector>
#include <cstdio>

namespace py = pybind11;

class Normalizer {
private:
    std::unordered_map<std::string, std::vector<double>> history;

public:
    double normalize_temperature(double value, const std::string& device_id) {

        printf("C++ normalize called\n");  // DEBUG ONLY

        double scaled = (value + 50.0) / 200.0;

        auto& h = history[device_id];
        h.push_back(scaled);

        if (h.size() > 5) {
            h.erase(h.begin());
        }

        double sum = 0.0;
        for (double v : h) sum += v;
        
        return sum / h.size();
    }

    double normalize_humidity(double value, const std::string& device_id) {
        printf("C++ normalize_humidity called\n");  // DEBUG ONLY
        double scaled = value / 100.0;

        auto& h = history[device_id];
        h.push_back(scaled);

        if (h.size() > 5) {
            h.erase(h.begin());
        }

        double sum = 0.0;
        for (double v : h) sum += v;
    
        return sum / h.size();
    }

    double normalize_pressure(double value, const std::string& device_id) {
        printf("C++ normalize_pressure called\n");  // DEBUG ONLY
        double scaled = (value - 300.0) / 800.0;

        auto& h = history[device_id];
        h.push_back(scaled);    
        if (h.size() > 5) {
            h.erase(h.begin());
        }
        
        double sum = 0.0;
        for (double v : h) sum += v;
       
        return sum / h.size();
    }
};

PYBIND11_MODULE(cpp_normalizer, m) {

    py::class_<Normalizer>(m, "Normalizer")
        .def(py::init<>())
        .def("normalize_temperature", &Normalizer::normalize_temperature)
        .def("normalize_humidity", &Normalizer::normalize_humidity)
        .def("normalize_pressure", &Normalizer::normalize_pressure);
}