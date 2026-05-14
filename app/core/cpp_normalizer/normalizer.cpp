#include <vector>
#include <unordered_map>
#include <string>
#include <numeric>

class Normalizer {
private:
    std::unordered_map<std::string, std::vector<double>> history;

public:
    double normalize_temperature(double value, const std::string& device_id) {

        double scaled = (value + 50.0) / 200.0;

        auto& h = history[device_id];
        h.push_back(scaled);

        if (h.size() > 5) {
            h.erase(h.begin());
        }

        double sum = std::accumulate(h.begin(), h.end(), 0.0);
        return sum / h.size();
    }
};