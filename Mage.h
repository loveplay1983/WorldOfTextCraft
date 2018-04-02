#ifndef Mage_h
#define Mage_h


 /*  __  __                   */
 /* |  \/  |                  */
 /* | \  / | __ _  __ _  ___  */
 /* | |\/| |/ _` |/ _` |/ _ \ */
 /* | |  | | (_| | (_| |  __/ */
 /* |_|  |_|\__,_|\__, |\___| */
 /*                __/ |      */
 /*               |___/       */

class Mage : public Entity{
 public :
   Mage( std::string name="", int attackPower=0 ) :
  Entity( "Mage", name, attackPower, 0, 0, 100) {
    };
  
    // In an attack, we reduce the hit points
    virtual int attack( Entity * other=0 ) {
      if ( other != 0 ) {
	setTarget(other);
      }

      if ( mana_ < 10 ) {
	std::cout << name() << " does not have enough mana." << std::endl;
	return 0;
      }
      
      if ( getTarget() != 0 ) {
	if ( getTarget()->isDead() ) {
	  std::cout << name_ << " : target " << getTarget()->name() << " is already dead." << std::endl;
	  return 0;
	}

	int ap = this->attackPower_;
	if ( getTurn() % 4 == 0 )
	  ap += 10;
	std::cout << name() << " attacks " << getTarget()->name() << " with attack power " << ap << std::endl;
	mana_ -= 10; 
	return getTarget()->reduceHitPoints( ap );
      } else {
	std::cout << name_ << " does not have a target to attack." << std::endl;
	return 0;
      }
   };
};

#endif
