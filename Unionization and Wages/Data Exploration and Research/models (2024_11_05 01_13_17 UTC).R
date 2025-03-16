library(tidyverse) 
library(broom)
library(knitr)
library(dplyr)
load(total_con)
load(total_manf)

#Wages of Time, very simple model
ggplot(total_con)+
  geom_point(aes(Year, UnWage, color="Union Wages"))+
  geom_point(aes(Year, NonWage, color="Nonunion Wages"))+
  ggtitle("Construction Wages over Time")+ 
  xlab("Years since 1972")+
  ylab("Hourly Wages")+
  labs(color="Union vs. Nonunion")

ggplot(total_manf)+ 
  geom_point(aes(Year, UnWage, color="Union Wages"))+
  geom_point(aes(Year, NonWage, color="Nonunion Wages"))+
  ggtitle("Manufacturing Wages over Time")+ 
  xlab("Years since 1972")+
  ylab("Hourly Wages")+
  labs(color="Union vs. Nonunion")

#Union wages on Nonunion wages 
##Construction
total_con3 <- mutate(total_con, Unroc= 100* (UnWage - lag(UnWage))/lag(UnWage), Nonroc= 100*(NonWage - lag(NonWage))/lag(NonWage))
total_con3 <- total_con3[-c (1),]

fit_con <- lm(Nonroc ~ Unroc, data=total_con3)
tidy(fit_con)%>%
  kable()
total_con1 <- augment(fit_con, data=total_con3)
ggplot(total_con1)+
  geom_point(aes(Unroc, Nonroc))+
  geom_line(aes(Unroc, .fitted))+
  ggtitle("Effect of Union Wage RoC on Nonunion Wage RoC")+ 
  xlab("Union Wage Rate of Change")+
  ylab("Nonunion Wage Rate of Change")
##Manufacturing
total_manf1 <- mutate(total_manf, Unroc= 100* (UnWage - lag(UnWage))/lag(UnWage), Nonroc= 100*(NonWage - lag(NonWage))/lag(NonWage))
total_manf1 <- total_manf1[-c (1),]

fit_manf <- lm(Nonroc ~ Unroc, data=total_manf1)
tidy(fit_manf)%>%
  kable()
total_manf2 <- augment(fit_manf, data=total_manf1)
ggplot(total_manf2)+
  geom_point(aes(Unroc, Nonroc))+
  geom_line(aes(Unroc, .fitted))+
  ggtitle("Effect of Union Wage RoC on Nonunion Wage RoC")+ 
  xlab("Union Wage Rate of Change")+
  ylab("Nonunion Wage Rate of Change")

#Union Membership on differences 
fit_con1 <- lm(Diff ~ PerMem, data=total_con)
tidy(fit_con1)%>%
  kable()
total_con2 <-augment(fit_con1, data=total_con)
ggplot(total_con2)+
  geom_point(aes(PerMem, Diff))+
  geom_line(aes(PerMem, .fitted))+
  ggtitle("Effect of Union Membership on Differences in Wages")+ 
  xlab("Union Membership Percentage")+
  ylab("Difference in Union and Nonunion Wages")

fit_con2 <- lm(Unroc ~ PerMem, data=total_con3)
tidy(fit_con2) %>%
  kable()
total_con4 <- augment(fit_con2, data=total_con3)
ggplot(total_con4)+
  geom_point(aes(PerMem, Unroc))+
  geom_line(aes(PerMem, .fitted))+
  ggtitle("Effect of Union Membership on Union Wage RoC")+ 
  xlab("Union Membership Percentage")+
  ylab("Union Wage Rate of Change")

fit_con3 <- lm(Nonroc ~ PerMem, data=total_con3)
tidy(fit_con3) %>%
  kable()
total_con5 <- augment(fit_con3, data=total_con3)
ggplot(total_con5)+
  geom_point(aes(PerMem, Nonroc))+
  geom_line(aes(PerMem, .fitted))+
  ggtitle("Effect of Union Membership on Union Wage RoC")+ 
  xlab("Union Membership Percentage")+
  ylab("Union Wage Rate of Change")

fit_manf1 <- lm(Diff ~ PerMem, data=total_manf)
tidy(fit_manf1)%>%
  kable()
total_manf2 <- augment(fit_manf1, data=total_manf)
ggplot(total_manf2)+
  geom_point(aes(PerMem, Diff))+
  geom_line(aes(PerMem, .fitted))+
  ggtitle("Effect of Union Membership on Differences in Wages")+ 
  xlab("Union Membership Percentage")+
  ylab("Difference in Union and Nonunion Wages")

fit_manf2 <- lm(Unroc ~ PerMem, data=total_manf1)
tidy(fit_manf2) %>%
  kable()
total_manf3 <- augment(fit_manf2, data=total_manf1)
ggplot(total_manf3)+
  geom_point(aes(PerMem, Unroc))+
  geom_line(aes(PerMem, .fitted))+ 
  ggtitle("Effect of Union Membership on Union Wage RoC")+ 
  xlab("Union Membership Percentage")+
  ylab("Union Wage Rate of Change")

fit_manf3 <- lm(Nonroc ~ PerMem, data=total_manf1)
tidy(fit_manf3) %>%
  kable()
total_manf4 <- augment(fit_manf3, data=total_manf1)
ggplot(total_manf4)+
  geom_point(aes(PerMem, Nonroc))+
  geom_line(aes(PerMem, .fitted))+
  ggtitle("Effect of Union Membership on Nonunion Wage RoC")+ 
  xlab("Union Membership Percentage")+
  ylab("Nonunion Wage Rate of Change")