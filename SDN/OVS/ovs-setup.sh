#! /usr/bin/bash

# This program was created by Axel Vazquez Montano for the Communication Networks Course 
#	(Instructor Dr. Michael McGarry) at the University of Texas at El Paso.
#
# *** Open Vswitch Setup Wizard ***
# This program contains an interacrive menu with the function of setting up an 
# open vSwitch for SDN development.
# Sudo privileges are needed to run some of the commands in this program.

#######################################################
# GLOBAL VARIABLES
#######################################################
show_ovs=1
create_bridge=2
add_ports=3
config_controller=4
exit_choice=5

#######################################################
# Function shows OVS information and configuration
# ARGUMENTS:
#	None
# OUTPUTS:
#	OVS info and config
# RETURN:
#	0 if successful
#######################################################
show_ovs_config() {
	ovs-vsctl show
	echo ""
	echo "*** Network Routes ***"
	route -n
	echo ""
}

#######################################################
# Function creates a bridge, connects automatically to
#	the IP stack
# ARGUMENTS:
#	usr_bridge - User input for bridge name.
#	operstate  - contains the operstate of the bridge
#	port_direct_addition - User input, decision to add
#						a port after creating the bridge
# OUTPUTS:
#	Feedback for the operstate of the added bridge
# RETURN:
#	0 if successful
#######################################################
create_ovs_bridge() {
	echo -ne "Would you like to add or delete a bridge? (add/del) "
	read add_del_bridge
	if [ "$add_del_bridge" == "add" ]; then
		echo "You are adding a bridge, please make sure you follow the format: br<n>
where n is the bridge number (ie. br0, br1 and so on)"
		echo -ne "Enter the name of the bridge you want to add: "
		read usr_bridge
		ovs-vsctl --may-exist add-br $usr_bridge
		echo "*** Created Bridge ***"
		echo "*** Enabling OpenFlow 1.0 on $usr_bridge ***"
		ovs-ofctl -O OpenFlow13 dump-flows $usr_bridge
		ovs-vsctl set bridge $usr_bridge protocols=OpenFlow10
		echo "*** OpenFlow 1.0 Enabled ***"
	
		echo "*** Checking $usr_bridge operstate ***"
		operstate=$(cat /sys/class/net/$usr_bridge/operstate)
		if [ "$operstate" == "down" ]; then
			echo "*** Configuring $usr_bridge as UP ***"
			ifconfig $usr_bridge up
			ifconfig $usr_bridge
			echo "*** $usr_bridge is UP ***"
		else
			echo "*** Bridge $usr_bridge is already up ***"
		fi

		echo -ne "Would you like to add a port to $usr_bridge? (y/n) "
		read port_direct_addition
		if [ "$port_direct_addition" == "y" ]; then
			add_ports_2bridge
		fi
	elif [ "$add_del_bridge" == "del" ]; then
		echo "*** You are deleting a bridge ***"
		basename -a /sys/class/net/br*
		echo -ne "Enter the name of one of the bridges above you want to delete: "
		read usr_del_bridge
		ovs-vsctl del-br $usr_bridge
		echo "*** Bridge Deleted ***"
	else
		echo "*** Invalid selection, please enter 'add' or 'del' only. Bridge not deleted ***"
	fi
}

#######################################################
# Function adds ports to the OVS bridge
# ARGUMENTS:
#	usr_add_ni - User input, contains the name of the 
#				 network interface to add as a port
#	bridge_no  - contains the bridge to add the port to
# OUTPUTS:
#	ifconfig for the bridge and port number
# RETURN:
#	0 if successful
#######################################################
add_ports_2bridge() {
	echo "*** Which of the following network interface do you wish to add to the bridge? ***"
	basename -a /sys/class/net/enp*
	echo -ne "Enter a network interface name as they're shown above: "
	read usr_add_ni
	basename -a /sys/class/net/br*
	echo -ne "Enter the bridge (shown above) you want to add the port to: "
	read bridge_no
	echo "*** Adding port: $usr_add_ni to bridge $bridge_no ***"
	ovs-vsctl add-port $bridge_no $usr_add_ni
	echo "*** Zeroing out $usr_add_ni interface ***"
	echo "*** and slap it on $bridge_no interface  ***"
	ifconfig $usr_add_ni 0
	echo "*** Would you like to assign an IP Address to $bridge_no? ***"
	echo "*** NOTE: Only select 'y' if the port is connected to internet! or if $bridge_no does not have an IP address yet! ***"
	read assign_IP_sel
	if [ "$assign_IP_sel" == "y" ]; then
		echo "*** Giving $bridge_no an IP address via DHCP ***"
		dhclient $bridge_no
		ifconfig $bridge_no && ifconfig $usr_add_ni
	fi
}

#######################################################
# Function connects bridge to SDN controller
# ARGUMENTS:
#	ip_addr - User input, contains the controller IP Address
#	port_no - User input, contains the controller port number
# OUTPUTS:
#	None
# RETURN:
#	0 if successful
#######################################################
configure_controller(){
	echo "*** SDN Controller IP address and port number ***"
	echo -ne "Enter the SDN controller IP address: "
	read ip_addr
	echo -ne "Enter the controller port number: "
	read port_no
	ovs-vsctl set-controller br0 tcp:"$ip_addr":$port_no
}

#######################################################
# Main function, displays options for user to chose.
# Calls the needed functions based on the user choice. 
# ARGUMENTS:
#	usr_choice - Contains the menu choice from the user
# GLOBAL VARIABLES:
#	Options for user are defined globally:
#	 	-> show_ovs
#		-> create_bridge
#		-> add_ports
#		-> config_controller
#		-> exit_choice
# OUTPUTS:
#	Menu with options
# 	Feedback if user entered another option other than 
#		the ones in the menu
# RETURN:
#	0 if successful
#######################################################
main_menu () {
    exit_flag=False
    while [ $exit_flag != True ]
    do
	echo -ne " 
		*** Open vSwitch (OVS) Setup Wizard ***		
	See the available options below:	
		(1) Show OVS configuration
		(2) Create/delete OVS bridge
		(3) Add ports to OVS bridge
		(4) Configure SDN controller
		(5) Exit Open vSwitch (OVS) Setup Wizard
		
	Enter a number option: "
		read usr_choice
	echo ""
        if [ $usr_choice -eq $show_ovs ]; then
			show_ovs_config
		elif [ $usr_choice -eq $create_bridge ]; then
			create_ovs_bridge
		elif [ $usr_choice -eq $add_ports ]; then
			add_ports_2bridge
		elif [ $usr_choice -eq $config_controller ]; then
			configure_controller
		elif [ $usr_choice -eq $exit_choice ]; then
			exit_flag=True
			echo " *** Closing Open vSwitch (OVS) Setup Wizard *** "
		else
			echo "********** Error: Number selection not recognized, please select a number from the menu **********"
		fi
	done
}

main_menu
