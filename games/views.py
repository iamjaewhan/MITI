from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404 

from users.serializers import BaseUserSerializer
from utils.permissions import IsOwner, IsParticipant

from .models import *
from .serializers import *

# Create your views here.
class GameListView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """_summary_
        경기 목록 조회

        Returns:
            Response:
                200 : 요청 정상 처리
                401 : 유효하지 않은 access token
        """
        queryset = Game.objects.all()
        serializer = BaseGameSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """_summary_
        경기 등록
        
        request body:
        {
            "invitation": <int:초대 인원수>,
            "start_datetime":"yyyy-mm-dd hh:mm",
            "end_datetime":"yyyy-mm-dd hh:mm",
            "address":"주소",
            "info":"전달 사항"
        }

        Returns:
            Response: 
                201 : 요청 정상 처리
                400 : 유효하지 않은 데이터 입력
                401 : 유효하지 않은 access token
        """
        request.data['host'] = request.user.id
        serializer = GameRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            game = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        
        
class GameDetailView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj = get_object_or_404(Game.objects.all(), id=self.kwargs['game_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, game_id):
        """_summary_
        경기 상세 조회

        Args:
            game_id (integer): 경기 ID

        Returns:
            Response :
                200 : 요청 정상 처리
                404 : 유효하지 않은 game_id
        """
        game = self.get_object()
        if game:
            serializer = BaseGameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)               


class PlayerListView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """_summary_
        해당 경기 인스턴스를 반환하는 메소드.
        
        Returns:
            Game objects: 경기 객체
            raise:
                404: 요청한 경기 id가 존재하지 않을 경우 
        """
        obj = get_object_or_404(Game.objects.all(), id=self.kwargs['game_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_players(self, game_obj):
        """_summary_
        인자로 전달받은 경기의 참여자들을 리스트화하여 반환

        Args:
            game_obj (game 모델 객체): 조회할 경기

        Returns:
            list : 경기 참여자 모델 객체들의 리스트
        """
        queryset = Participation.objects.filter(game=game_obj)
        return list(map(lambda x:x.user, queryset))
        
    def get(self, request, game_id):
        """_summary_
        경기 참여 유저 리스트 조회
        
        Args:
            game_id (integer): 게임 ID

        Returns:
            Response: 
                200 : 요청 정상 처리
                401 : 유효하지 않은 access token
                404 : 유효하지 않은 game_id
        """
        game_obj = self.get_object()
        user_objs = self.get_players(game_obj)
        data = {
            'game': BaseGameSerializer(game_obj).data,
            'users': BaseUserSerializer(user_objs, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, game_id):
        """_summary_
        경기 참여

        Args:
            game_id (integer): 경기 ID

        Returns:
            Response: 
                201 : 요청 정상 처리
                400 : 중복 참여 신청
                401 : 유효하지 않은 access_token
                404 : 유효하지 않은 game_id
        """
        data = {
            'game': game_id,
            'user': request.user.id
        }
        serializer = ParticipationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class PlayerDetailView(views.APIView):
    
    def get_object(self):
        """_summary_
        participation 객체를 반환하며 check_object_permissions() 호출하여
        해당 유저의 permission 점검

        Returns:
            participation objects: 경기 참여 신청 객체 
        """
        obj = Participation.objects.get(game_id=self.kwargs['game_id'], user_id=self.kwargs['user_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_permissions(self):
        """_summary_
        요청에 따른 permission_classes 설정
        
        GET : IsParticipant
        DELETE : IsOwner
        """
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsParticipant]
        elif self.request.method == 'DELETE':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
    
    def get(self, request, game_id, user_id):
        """_summary_

        Args:
            game_id (integer): 경기 ID
            user_id (integer): 유저 ID

        Returns:
            Response: 
                200 : 요청 정상 처리
                401 : 유효하지 않은 access token
        """
        obj = self.get_object()
        serializer = BaseUserSerializer(obj.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, game_id, user_id):
        """_summary_

        Args:
            game_id (integer): 경기 ID
            user_id (integer): 유저 ID

        Returns:
            Response: 
                200 : 요청 정상 처리
                401 : 유효하지 않은 access token
                403 : 사용자의 데이터가 아닌 경우
                404 : 유효하지 않은 game_id 혹은 user_id
        """
        obj = self.get_object()
        serializer = ParticipationSerializer(obj)
        serializer.delete()
        return Response(status=status.HTTP_200_OK)
    


from payment.payment import KakaoPayClient, KakaoPayReadyDto, KakaoPayApprovalDto
from payment.models import *
from constants.custom_exceptions import *


class ParticipationPaymentView(views.APIView):
    permission_classes = [IsOwner]
        
    def get_object(self):
        obj = get_object_or_404(Participation.objects.all(), id=self.kwargs['participation_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_or_create_payment_request(self, participation_obj):
        """_summary_
        Participation에 해당하는 PaymentRequest 인스턴스를 반환하는 메소드
        
        Returns:
            ParticipationRequest 인스턴스
        """
        payment_request_queryset = ParticipationPaymentRequest.objects.filter(
            participation=participation_obj)
        
        # 기존의 request 기록이 존재하는 경우
        if payment_request_queryset.exists():
            payment_request_obj = payment_request_queryset.select_related('payment_result').first()
            payment_result = payment_request_obj.payment_result
            
            # 기존의 요청이 결제가 완료된 경우
            if payment_result.status == PaymentStatus.APPROVED:
                raise DuplicatedPaymentException()
            
            # 기존 결제 요청 상태가 READY가 아닌 경우
            if payment_result.status != PaymentStatus.READY:
                # 기존 결제 요청 상태 변경 구현
                pass

        # 기존의 request 기록이 존재하지 않는 경우 -> request생성 
        else:
            payment_request_serializer = ParticipationPaymentRequestSerializer(
                data={'participation': participation_obj.id})
            
            if payment_request_serializer.is_valid(raise_exception=True):
                payment_request_obj = payment_request_serializer.save()
                
        return payment_request_obj
            

    def post(self, request, game_id, participation_id):

        participation_obj = self.get_object()
        payment_request_obj = self.get_or_create_payment_request(participation_obj)
        ready_dto = KakaoPayReadyDto(payment_request_obj)
    
        kakao_client = KakaoPayClient()
        ready_dto = kakao_client.ready(ready_dto)
        ready_dto.add_param('participation', participation_id)
        payment_request_serializer = ParticipationPaymentRequestSerializer(
            payment_request_obj, data=ready_dto.get_params())
                
        if payment_request_serializer.is_valid(raise_exception=True):
            payment_request_serializer.save()

        return Response(
            {
                'payment_information': PaymentInfoSerializer(ready_dto.get_params()).data,
                'payment_urls': PaymentRedirectUrlSerializer(ready_dto.get_params()).data
            },
            status = status.HTTP_200_OK
        )


class KakaoPaymentApprovalCallbackView(views.APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request, game_id, user_id):
        
        participation_queryset = Participation.objects.filter(game=game_id, user=user_id)
        
        if not participation_queryset.exists():
            raise NotFound("해당되는 참여 신청이 없습니다.")
        
        participation = participation_queryset.first()
        payment_request_queryset = ParticipationPaymentRequest.objects.filter(participation=participation)
        
        if not payment_request_queryset.exists():
            raise NotFound("해당되는 결제 신청이 없습니다.")
    
        payment_request = payment_request_queryset.first()
        
        payment_result_queryset = ParticipationPaymentResult.objects.filter(payment_request=payment_request)
            
            
            ## PaymentResult 객체를 생성하거나 기존에 존재하던 객체 가져오기
        if payment_result_queryset.exists():
            payment_result = payment_result_queryset.first()
        else:
            data = PaymentResultBuilder.build(payment_request)
            result_serializer = ParticipationPaymentResultSerializer(
                data=PaymentResultBuilder.build(payment_request))
            if result_serializer.is_valid(raise_exception=True):
                payment_result = result_serializer.save()
 
        approval_request = KakaoPayApprovalDto(payment_request, request.GET.get('pg_token', None))
        approval_request.set_param('participation', participation.id)
        response_data = KakaoPayClient.approve(approval_request)
        result_serializer = ParticipationPaymentResultSerializer(
            payment_result, data=response_data.get_params()
        )
        
        if result_serializer.is_valid(raise_exception=True):
            payment_result = result_serializer.save()
            return Response(result_serializer.data, status=status.HTTP_200_OK)


class KakaoPaymentFailCallbackView(views.APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request, game_id, user_id):
        return Response(data={"message": "fail callback "}, status=status.HTTP_200_OK)
        

class KakaoPaymentCancelCallbackView(views.APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request, game_id, user_id):
        return Response(data={"message": "cancel callback "}, status=status.HTTP_200_OK)

        
            