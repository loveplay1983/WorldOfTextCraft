#ifndef Rogue_h
#define Rogue_h


 /*  _____                         */
 /* |  __ \                        */
 /* | |__) |___   __ _ _   _  ___  */
 /* |  _  // _ \ / _` | | | |/ _ \ */
 /* | | \ \ (_) | (_| | |_| |  __/ */
 /* |_|  \_\___/ \__, |\__,_|\___| */
 /*               __/ |            */
 /*              |___/             */

class Rogue : public Entity{
 public :
   Rogue( std::string name="", int attackPower=0, int bonus=7 ) :
    Entity( "Rogue", name, attackPower, 0, 0), bonus_(bonus) {
    };
  
   // In an attack, we reduce the hit points
   virtual int attack( Entity * other=0 ) {

     if ( other != 0 ) {
       setTarget(other);
     }

     if ( getTarget() != 0 ) {
       if ( getTarget()->isDead() ) {
	 std::cout << name_ << " : target " << getTarget()->name() << " is already dead." << std::endl;
	 return 0;
       }

       int ap = this->attackPower_ + this->bonus_ * (this->getTurn()%2);
       std::cout << name() << " attacks " << getTarget()->name() << " with attack power " << ap << std::endl;
       return getTarget()->reduceHitPoints( ap );
     } else {
       std::cout << name_ << " does not have a target to attack." << std::endl;
       return 0;
     }
     
   };
 protected :
   int bonus_;
};

#endif
