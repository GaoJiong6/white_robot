#include <memory> // C++智能指针（如std::shared_ptr）
#include <string.h>
#include <string>    // C++字符串类
#include "rclcpp/rclcpp.hpp" // ROS 2核心库（节点、订阅等）
#include "geometry_msgs/msg/twist.hpp"
using std::placeholders::_1; // 占位符，用于回调函数绑定

class MinimalSubscriber : public rclcpp::Node
{
  public:
    MinimalSubscriber()
    : Node("minimal_subscriber")
    {
    subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(
    "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    }

  private:
    void topic_callback(const geometry_msgs::msg::Twist::SharedPtr twist_aux)
    {
      RCLCPP_INFO(this->get_logger(),"not akm");
    }
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}
