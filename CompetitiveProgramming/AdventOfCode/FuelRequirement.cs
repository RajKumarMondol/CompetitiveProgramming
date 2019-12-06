using System;

namespace CompetitiveProgramming.AdventOfCode
{
    public class FuelRequirement
    {
        public long calculateFuelForMass(int[] moduleMasses)
        {
            long totalFuelRequirement = 0;
            foreach (int moduleMass in moduleMasses)
            {
                totalFuelRequirement += getFuelRequirementForMass(moduleMass);
            }
            return totalFuelRequirement;
        }

        private int getFuelRequirementForMass(int moduleMass)
        {
            return (moduleMass / 3 - 2);
        }

        public long calculateFuelForMassAndFuel(int[] moduleMasses)
        {
            long totalFuelRequirement = 0;
            foreach (int moduleMass in moduleMasses)
            {
                totalFuelRequirement += getFuelRequirementForMassAndFuel(moduleMass);
            }
            return totalFuelRequirement;
        }

        private int getFuelRequirementForMassAndFuel(int moduleMassOrFuelMass)
        {
            int fuelMass = getFuelRequirementForMass(moduleMassOrFuelMass);
            if (fuelMass <= 0) return 0;
            else return (fuelMass + getFuelRequirementForMassAndFuel(fuelMass));
        }
    }
}