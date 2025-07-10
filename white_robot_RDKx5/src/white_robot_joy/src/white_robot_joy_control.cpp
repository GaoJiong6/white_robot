#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "std_msgs/msg/float64.hpp"
#include<iostream>
using std::placeholders::_1;
using namespace std;
class white_robot_joy : public rclcpp::Node
{
   rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr sub_cmd_vel;

public:
    white_robot_joy()
        : Node("white_robot_joy")
    {
        sub_cmd_vel = this->create_subscription<geometry_msgs::msg::Twist>(
            "cmd_vel", 2, std::bind(&white_robot_joy::Cmd_Vel_Callback, this, _1));
} 

private:
    void Cmd_Vel_Callback(const geometry_msgs::msg::Twist::SharedPtr twist_aux)
    {
        printf("1111111\n");
    }
 
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<white_robot_joy>());
    return 0;
}
