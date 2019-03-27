/// @file main.cpp
/// @brief Udemy Patterns Lesson 1
/// @author Reinaldo Molina
/// @version  0.0
/// @date Mar 05 2019
// Copyright © 2019 Reinaldo Molina

// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
// OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
// OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/cURLpp.hpp>
#include <fstream>

int main(int, const char **) {
  try {
    // That's all that is needed to do cleanup of used resources (RAII style).
    curlpp::Cleanup cleanup;

    // Our request to be sent.
    curlpp::Easy request;

    // Set the URL.
    request.setOpt<curlpp::options::Url>("http://example.com");

    request.setOpt<curlpp::options::HttpAuth>(123556456);

    // Send request and get a result.
    // By default the result goes to standard output.
    std::ofstream ofs("out_request");
    ofs << request;

	return 0;
  } catch (curlpp::RuntimeError &e) {
    std::cout << e.what() << std::endl;
    return 1;
  } catch (curlpp::LogicError &e) {
    std::cout << e.what() << std::endl;
    return 2;
  }

  return 0;
}
