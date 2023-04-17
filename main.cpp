#include <SFML/Graphics.hpp>

#include <SFML/Graphics/RenderWindow.hpp>

#include <SFML/System/Vector2.hpp>

#include <SFML/Window/Event.hpp>
#include <SFML/Window/Mouse.hpp>
#include <SFML/Window/Window.hpp>

#include <cmath>

#include <functional>

#include <iostream>

#include <math.h>

#include <utility>



std::vector<std::pair<float, float>> create_parametric_curve() {

  int nsteps = 1000;

  float t = 0.f;

  float r = 100.f;

  float step = 2 * M_PI / nsteps;



  std::vector<std::pair<float, float>> curve;

  for (int i = 0; i < nsteps; i++) {

    float x = sin(t) * r + 200.f;

    float y = cos(t) * r + 200.f;

    curve.push_back(std::pair<float, float>(x, y));



    t += step;

  }



  return curve;

}



std::vector<std::pair<float, float>>

create_sine_wave(float x_start, float x_end, float step, float shift) {

  std::vector<std::pair<float, float>> sine_wave;

  int nsteps = (int)((x_end - x_start) / step);



  float x = x_start;

  float y = sin(x);



  for (int i = 0; i < nsteps; i++) {

    std::pair<float, float> point(x, y);

    sine_wave.push_back(point);



    x += step;

    y = sin((x + shift) * (M_PI / 180.f)) * 100 + 200;

  }



  return sine_wave;

}



std::vector<std::pair<sf::Vector2i, sf::Vector2i>>

connect_dots(std::vector<sf::Vector2i> dots) {

  std::vector<std::pair<sf::Vector2i, sf::Vector2i>> curve;

  for (int i = 0; i < dots.size(); i++) {

    curve.push_back(std::pair<sf::Vector2i, sf::Vector2i>(

        dots[i], dots[(i + 1) % dots.size()]));

  }



  return curve;

}



void draw(std::vector<sf::Vector2i> points, sf::RenderWindow &window) {

  for (auto point : points) {

    sf::CircleShape dot(2.f);

    dot.setFillColor(sf::Color::Green);

    dot.move(point.x, point.y);

    window.draw(dot);

  }

}



void draw(std::vector<std::pair<sf::Vector2i, sf::Vector2i>> lines,

          sf::RenderWindow &window) {

  for (auto pair : lines) {

    auto point_a = pair.first;

    auto point_b = pair.second;



    sf::Vertex line[] = {

        sf::Vertex(sf::Vector2f(point_a.x, point_a.y)),

        sf::Vertex(sf::Vector2f(point_b.x, point_b.y)),

    };

    line->color = sf::Color::Red;

    window.draw(line, 2, sf::Lines);

  }




}


int main() {

  /* Antialiasing */

  sf::ContextSettings settings;

  settings.majorVersion = 2;

  settings.minorVersion = 0;

  settings.antialiasingLevel = 4;



  sf::RenderWindow window(sf::VideoMode(400, 400), "Curves Editor",

                          sf::Style::Default, settings);

  float shift = 0.f;



  std::vector<sf::Vector2i> points;



  while (window.isOpen()) {

    sf::Event event;

    while (window.pollEvent(event)) {

      if (event.type == sf::Event::Closed)
      {
        window.close();
      }
      
      static bool lock_click = false;
      if (sf::Event::MouseButtonPressed && !lock_click) {
        sf::Vector2i position = sf::Mouse::getPosition(window);
        points.push_back(position);
        lock_click = true;
      }

      if (event.type == sf::Event::MouseButtonReleased &&
          event.mouseButton.button == sf::Mouse::Left) {
        lock_click = false;
      }
    }
    
   shift += 0.5;
    auto sine_wave = create_sine_wave(0.f, 1000.f, 0.1f, shift);
    auto curve = create_parametric_curve();
    window.clear();

    for (int i = 0; i + 1 < curve.size(); i++) {
      auto point_a = curve[i];
      auto point_b = curve[i + 1];

      sf::Vertex line[] = {
          sf::Vertex(sf::Vector2f(point_a.first, point_a.second)),
          sf::Vertex(sf::Vector2f(point_b.first, point_b.second)),
      };
      line->color = sf::Color::Green;
      window.draw(line, 2, sf::Lines);
    }

    auto lines = connect_dots(points);

    draw(points, window);
    draw(lines, window);

    window.display();
  }
    return 0;
  }

